#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用例36：心跳状态监视器
监控所有自动化任务是否正常运行
"""

import os
import json
from datetime import datetime, timedelta

STATE_FILE = os.path.expanduser("~/.openclaw/workspace/memory/heartbeat-state.json")

# 任务阈值（分钟）
THRESHOLDS = {
    "default": 120,  # 默认2小时
    "critical": 60,   # 关键任务1小时
    "warning": 180,   # 警告3小时
}

def load_state():
    """加载心跳状态"""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {}

def format_time_ago(timestamp):
    """格式化时间差"""
    if not timestamp:
        return "未知"
    
    dt = datetime.fromtimestamp(timestamp / 1000)
    diff = datetime.now() - dt
    
    minutes = int(diff.total_seconds() / 60)
    
    if minutes < 60:
        return f"{minutes}分钟前"
    elif minutes < 1440:
        return f"{minutes // 60}小时{minutes % 60}分钟前"
    else:
        return f"{minutes // 1440}天前"

def check_task_status(name, last_run, threshold):
    """检查任务状态"""
    if not last_run:
        return "⚪ 未运行", "unknown"
    
    dt = datetime.fromtimestamp(last_run / 1000)
    diff = datetime.now() - dt
    minutes = int(diff.total_seconds() / 60)
    
    if minutes > threshold:
        return "🔴 超时", "critical"
    elif minutes > threshold * 0.8:
        return "🟡 即将超时", "warning"
    else:
        return "✅ 正常", "normal"

def run_monitor():
    """运行监控"""
    print(f"\n💓 心跳状态监视器")
    print("="*50)
    print(f"检查时间: {datetime.now().strftime('%H:%M:%S')}")
    print("="*50)
    
    state = load_state()
    
    if not state:
        print("❌ 无心跳状态数据")
        return
    
    alerts = []
    
    print("\n📊 任务状态:\n")
    
    for task, data in state.items():
        if isinstance(data, dict):
            last = data.get('lastCheck') or data.get('lastRun') or data.get('timestamp')
        else:
            last = None
        
        threshold = data.get('threshold', THRESHOLDS['default']) if isinstance(data, dict) else THRESHOLDS['default']
        
        status, level = check_task_status(task, last, threshold)
        time_ago = format_time_ago(last) if last else "从未运行"
        
        print(f"{status} {task}")
        print(f"   上次运行: {time_ago}")
        
        if level in ['critical', 'warning']:
            alerts.append((task, status, time_ago))
    
    print("\n" + "="*50)
    
    if alerts:
        print(f"\n⚠️ 发现 {len(alerts)} 个问题:")
        for task, status, time_ago in alerts:
            print(f"   {status} {task} ({time_ago})")
    else:
        print("\n✅ 所有任务正常运行！")
    
    return len(alerts) == 0

def main():
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        run_monitor()
    else:
        print("💓 心跳状态监视器")
        print("\n用法: python heartbeat_monitor.py check")
        print("或者配置Cron定时运行")

if __name__ == "__main__":
    success = run_monitor()
    exit(0 if success else 1)

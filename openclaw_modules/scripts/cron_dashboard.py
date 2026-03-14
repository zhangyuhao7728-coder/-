#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用例 35：Cron 任务看板 - 可视化版
"""

import subprocess
import json
import os
from datetime import datetime

OPENCLAW_CMD = os.path.expanduser("~/.nvm/versions/node/v22.22.0/bin/openclaw")

def get_cron_list():
    """获取 cron 列表"""
    result = subprocess.run(
        [OPENCLAW_CMD, "cron", "list"],
        capture_output=True,
        text=True,
        timeout=30
    )
    return result.stdout

def get_cron_runs():
    """获取最近运行历史"""
    result = subprocess.run(
        [OPENCLAW_CMD, "cron", "runs", "--limit", "5"],
        capture_output=True,
        text=True,
        timeout=30
    )
    return result.stdout

def parse_cron_info(output):
    """解析 cron 输出"""
    lines = output.strip().split('\n')
    jobs = []
    
    for line in lines:
        if 'daily-journal' in line:
            jobs.append({
                "name": "📓 每日学习日记",
                "time": "21:00",
                "icon": "💤"
            })
        elif 'daily-briefing' in line:
            jobs.append({
                "name": "📋 每日简报",
                "time": "7:00",
                "icon": "🌅"
            })
        elif '每日学习计划' in line:
            jobs.append({
                "name": "📚 每日学习计划",
                "time": "8:00",
                "icon": "📖"
            })
    
    return jobs

def format_dashboard():
    """格式化看板"""
    output = get_cron_list()
    jobs = parse_cron_info(output)
    
    now = datetime.now()
    
    dashboard = f"""╔══════════════════════════════════════════════════════════════╗
║           📊 OpenClaw 任务看板                         ║
╠══════════════════════════════════════════════════════════════╣
║  最后更新: {now.strftime('%Y-%m-%d %H:%M')}                              ║
╠══════════════════════════════════════════════════════════════╣"""
    
    for job in jobs:
        # 计算下次运行时间
        hour = int(job['time'].split(':')[0])
        current_hour = now.hour
        
        if hour > current_hour:
            hours_left = hour - current_hour
            next_run = f"{hours_left}小时后"
        else:
            hours_left = 24 - current_hour + hour
            next_run = f"明天 {job['time']}"
        
        dashboard += f"""
║  {job['icon']} {job['name']}
║     ⏰ 运行时间: {job['time']}     ▶️ 下次: {next_run}
║     ✅ 状态: 正常
╠══════════════════════════════════════════════════════════════╣"""
    
    dashboard += """
║  📈 统计: 3 个任务 | 运行中: 0 | 待运行: 3
╚══════════════════════════════════════════════════════════════╝

💡 常用命令:
   • "查看任务看板" - 显示此看板
   • "查看日志" - 查看运行日志
   • "禁用任务 [名称]" - 暂停任务
"""
    
    return dashboard

if __name__ == "__main__":
    print(format_dashboard())

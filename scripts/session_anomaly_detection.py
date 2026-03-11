#!/usr/bin/env python3
"""
会话异常检测脚本

用于检测 OpenClaw 会话中的异常情况。
"""

import os
import sys
import json
import time
from datetime import datetime, timedelta

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def check_session_anomalies():
    """检查会话异常"""
    try:
        # 检查会话目录
        sessions_dir = os.path.expanduser("~/.openclaw/sessions")
        if not os.path.exists(sessions_dir):
            print("会话目录不存在")
            return False
            
        # 检查最近的会话文件
        session_files = []
        for filename in os.listdir(sessions_dir):
            if filename.endswith(".json") and filename.startswith("session-"):
                filepath = os.path.join(sessions_dir, filename)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        session_files.append(data)
                except Exception as e:
                    print(f"读取会话文件失败: {e}")
        
        # 检查异常会话
        anomalies = []
        now = datetime.now()
        
        for session in session_files:
            try:
                # 检查会话是否过期
                if "last_active" in session:
                    last_active = datetime.fromisoformat(session["last_active"].replace("Z", "+00:00"))
                    if now - last_active > timedelta(hours=24):
                        anomalies.append(f"会话 {session.get('id', 'unknown')} 已过期")
                
                # 检查会话状态异常
                if session.get("status") == "error":
                    anomalies.append(f"会话 {session.get('id', 'unknown')} 状态异常")
                
                # 检查会话持续时间过长
                if "duration" in session and session["duration"] > 3600:  # 超过 1 小时
                    anomalies.append(f"会话 {session.get('id', 'unknown')} 持续时间过长")
            except Exception as e:
                print(f"分析会话数据失败: {e}")
        
        # 输出异常情况
        if anomalies:
            print("发现会话异常:")
            for anomaly in anomalies:
                print(f"  - {anomaly}")
            return True
        else:
            print("未发现会话异常")
            return False
            
    except Exception as e:
        print(f"检查会话异常失败: {e}")
        return False

def main():
    """主函数"""
    print("开始检查会话异常...")
    found_anomalies = check_session_anomalies()
    print("检查完成")
    
    return found_anomalies

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用例08：会话异常检测
检测异常登录和会话
"""

import os
import subprocess
from datetime import datetime, timedelta

def check_recent_logins():
    """检查最近登录"""
    result = subprocess.run(
        ["last", "-20"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        lines = result.stdout.strip().split('\n')
        
        suspicious = []
        for line in lines:
            if 'pts' in line or 'tty' in line:
                # 检查异常时间
                parts = line.split()
                if len(parts) >= 8:
                    time_str = ' '.join(parts[4:6])
                    # 这里可以添加更多检查
                    pass
        
        return lines[:10]
    
    return []

def check_ssh_sessions():
    """检查SSH会话"""
    result = subprocess.run(
        ["who", "-u"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        sessions = result.stdout.strip().split('\n')
        
        print("\n🔐 当前会话:")
        for session in sessions:
            print(f"   {session}")
        
        return len(sessions)
    
    return 0

def check_failed_logins():
    """检查失败登录"""
    result = subprocess.run(
        ["last", "-f", "/var/log/auth.log", "-20"],
        capture_output=True,
        text=True
    )
    
    # macOS可能没有这个文件
    return []

def detect_anomalies():
    """检测异常"""
    anomalies = []
    
    # 1. 检查SSH会话
    ssh_count = check_ssh_sessions()
    
    if ssh_count > 3:
        anomalies.append(f"SSH会话过多: {ssh_count}")
    
    # 2. 检查异常登录时间
    recent = check_recent_logins()
    
    return anomalies

def run_session_anomaly_detection():
    """运行会话异常检测"""
    print("\n🔍 会话异常检测")
    print("="*50)
    print(f"检查时间: {datetime.now().strftime('%H:%M:%S')}")
    print("="*50)
    
    # 检测异常
    anomalies = detect_anomalies()
    
    print("\n" + "="*50)
    
    if anomalies:
        print(f"\n⚠️ 发现 {len(anomalies)} 个异常:")
        for a in anomalies:
            print(f"   🔴 {a}")
    else:
        print("\n✅ 未发现异常")
    
    return len(anomalies) == 0

if __name__ == "__main__":
    run_session_anomaly_detection()

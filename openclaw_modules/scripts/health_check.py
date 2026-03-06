#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram 连接健康检查与自动修复
检测连接状态并自动修复
"""

import subprocess
import time
import os

def check_gateway():
    """检查 Gateway 状态"""
    result = subprocess.run(
        ["pgrep", "-f", "openclaw-gateway"],
        capture_output=True,
        text=True
    )
    return result.returncode == 0

def restart_gateway():
    """重启 Gateway"""
    print("🔄 正在重启 Gateway...")
    subprocess.run(["openclaw", "gateway", "restart"])
    time.sleep(5)
    return check_gateway()

def check_connection():
    """检查 Telegram 连接"""
    # 检查日志中的错误
    result = subprocess.run(
        ["openclaw", "logs", "--limit", "10", "--no-color"],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    if "sequence" in result.stdout.lower() or "gap" in result.stdout.lower():
        return "sequence_warning"
    
    if "error" in result.stdout.lower() and "telegram" in result.stdout.lower():
        return "telegram_error"
    
    return "ok"

def run_health_check():
    """运行健康检查"""
    print("🔍 正在检查系统状态...")
    
    # 1. 检查 Gateway
    if not check_gateway():
        print("❌ Gateway 未运行，正在启动...")
        restart_gateway()
    
    # 2. 检查 Telegram 连接
    status = check_connection()
    
    if status == "ok":
        print("✅ 所有服务正常")
    elif status == "sequence_warning":
        print("⚠️ 检测到序列号警告，尝试修复...")
        restart_gateway()
    else:
        print("⚠️ 检测到 Telegram 错误")
    
    return status

if __name__ == "__main__":
    run_health_check()

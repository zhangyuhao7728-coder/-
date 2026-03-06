#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram 连接自动修复脚本
检测并自动修复连接问题
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
    subprocess.run(["openclaw", "gateway", "restart"], capture_output=True)
    time.sleep(5)
    return check_gateway()

def fix_connection():
    """修复连接"""
    print("🔧 正在修复 Telegram 连接...")
    
    # 重启 Gateway
    if not restart_gateway():
        print("❌ 重启失败")
        return False
    
    print("✅ 连接已修复")
    return True

def main():
    """主函数"""
    print("🛠️ Telegram 连接自动修复")
    print("="*50)
    
    if not check_gateway():
        print("⚠️ Gateway 未运行，正在启动...")
        fix_connection()
    else:
        print("✅ Gateway 运行中")
        fix_connection()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Gateway 保活脚本
每5分钟检查一次，如果Gateway停止则自动重启
"""

import os
import subprocess
import time

def is_gateway_running():
    """检查Gateway是否运行"""
    result = subprocess.run(
        ["pgrep", "-f", "openclaw-gateway"],
        capture_output=True
    )
    return result.returncode == 0

def restart_gateway():
    """重启Gateway"""
    print("🔄 Gateway未运行，正在启动...")
    subprocess.Popen(
        ["nohup", os.path.expanduser("~/.nvm/versions/node/v22.22.0/bin/openclaw"), "gateway", "start"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(3)
    
    if is_gateway_running():
        print("✅ Gateway已启动")
        return True
    else:
        print("❌ 启动失败")
        return False

def main():
    if not is_gateway_running():
        restart_gateway()
    else:
        print("✅ Gateway运行正常")

if __name__ == "__main__":
    main()

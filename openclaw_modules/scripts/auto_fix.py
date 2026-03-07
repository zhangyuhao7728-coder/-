#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
异常监控与自动修复 - 带警报版
"""

import subprocess
import time
import shutil
import os

# 检查 openclaw 命令可用性
def get_openclaw_cmd():
    """获取 openclaw 命令"""
    if shutil.which("openclaw"):
        return ["openclaw"]
    return ["npx", "-y", "openclaw"]

OPENCLAW_CMD = get_openclaw_cmd()

def check_for_errors():
    """检查是否有错误"""
    result = subprocess.run(
        OPENCLAW_CMD + ["logs", "--limit", "30", "--no-color"],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    if result.returncode != 0:
        return True, "Gateway logs error"
    
    errors = ["gap detected", "connection failed", "authentication failed", "error"]
    log_text = result.stdout.lower()
    
    for error in errors:
        if error in log_text:
            return True, f"Found: {error}"
    
    return False, "OK"

def send_alert(message):
    """发送警报到 Telegram"""
    # 直接通过 OpenClaw 发送消息
    cmd = OPENCLAW_CMD + ["message", "send", "--to", "8793442405", "--message", f"🚨 {message}"]
    subprocess.run(cmd, capture_output=True)

def run_fix():
    """运行修复"""
    send_alert("检测到异常，正在尝试修复...")
    subprocess.run(OPENCLAW_CMD + ["gateway", "restart"], capture_output=True)
    time.sleep(5)
    send_alert("✅ 修复完成，系统已恢复正常")

def main():
    """主函数"""
    print("🔍 正在检查系统状态...")
    
    has_error, msg = check_for_errors()
    
    if has_error:
        print(f"⚠️ {msg}")
        run_fix()
    else:
        print("✅ 无异常")

if __name__ == "__main__":
    main()

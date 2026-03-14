#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw 自动维护脚本
- 检查配置错误
- 自动修复
- 备份配置
- 检查Gateway状态
"""

import os
import subprocess
import shutil
import json
from datetime import datetime

OPENCLAW_DIR = os.path.expanduser("~/.openclaw")
CONFIG_FILE = os.path.join(OPENCLAW_DIR, "openclaw.json")
BACKUP_DIR = os.path.join(OPENCLAW_DIR, "backups")
LOG_FILE = os.path.join(OPENCLAW_DIR, "logs", "auto_maintenance.log")

OPENCLAW_CMD = os.path.expanduser("~/.nvm/versions/node/v22.22.0/bin/openclaw")

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

def check_gateway():
    """检查Gateway状态"""
    print("\n🔍 检查Gateway状态...")
    code, out, err = run_cmd(f"{OPENCLAW_CMD} gateway status")
    
    if "running" in out.lower():
        print("   ✅ Gateway 运行正常")
        return True
    else:
        print("   ❌ Gateway 未运行，尝试启动...")
        run_cmd(f"{OPENCLAW_CMD} gateway start")
        return False

def check_config():
    """检查配置错误"""
    print("\n🔍 检查配置...")
    code, out, err = run_cmd(f"{OPENCLAW_CMD} doctor 2>&1")
    
    if "Config invalid" in out or "Unrecognized key" in out:
        print("   ⚠️ 发现配置错误，尝试修复...")
        run_cmd(f"{OPENCLAW_CMD} doctor --fix")
        return False
    
    print("   ✅ 配置正常")
    return True

def backup_config():
    """备份配置"""
    print("\n💾 备份配置...")
    
    if not os.path.exists(CONFIG_FILE):
        print("   ❌ 配置文件不存在")
        return False
    
    os.makedirs(BACKUP_DIR, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(BACKUP_DIR, f"openclaw_{timestamp}.json")
    
    shutil.copy2(CONFIG_FILE, backup_file)
    
    # 只保留最近5个备份
    backups = sorted([f for f in os.listdir(BACKUP_DIR) if f.startswith("openclaw_")])
    while len(backups) > 5:
        old = backups.pop(0)
        os.remove(os.path.join(BACKUP_DIR, old))
    
    print(f"   ✅ 已备份到: {backup_file}")
    return True

def check_ports():
    """检查端口"""
    print("\n🔍 检查端口...")
    code, out, err = run_cmd("lsof -i :18789")
    
    if "LISTEN" in out:
        print("   ✅ 端口18789正常监听")
        return True
    else:
        print("   ❌ 端口异常")
        return False

def restart_if_needed():
    """必要时重启"""
    print("\n🔄 检查是否需要重启...")
    
    code, out, err = run_cmd("pgrep -f openclaw-gateway")
    
    if code != 0:
        print("   ⚠️ Gateway未运行，正在启动...")
        run_cmd(f"{OPENCLAW_CMD} gateway start")
    else:
        print("   ✅ Gateway运行中")

def run_maintenance():
    """运行维护"""
    print("="*50)
    print("🛠️  OpenClaw 自动维护")
    print("="*50)
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. 备份配置
    backup_config()
    
    # 2. 检查配置
    check_config()
    
    # 3. 检查Gateway
    check_gateway()
    
    # 4. 检查端口
    check_ports()
    
    # 5. 必要时重启
    restart_if_needed()
    
    print("\n" + "="*50)
    print("✅ 维护完成")
    print("="*50)

if __name__ == "__main__":
    run_maintenance()

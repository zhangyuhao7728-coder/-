#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw 紧急检查脚本
遇到突发事件错误时立即执行
"""

import os
import subprocess

OPENCLAW_CMD = os.path.expanduser("~/.nvm/versions/node/v22.22.0/bin/openclaw")

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

def check_gateway():
    """检查Gateway"""
    print("🔍 检查 Gateway...")
    code, out, err = run_cmd(f"{OPENCLAW_CMD} gateway status")
    
    if "running" in out.lower():
        print("   ✅ Gateway 运行正常")
        return True
    else:
        print("   ❌ Gateway 异常，尝试启动...")
        run_cmd(f"{OPENCLAW_CMD} gateway start")
        return False

def check_config():
    """检查配置"""
    print("🔍 检查配置...")
    code, out, err = run_cmd(f"{OPENCLAW_CMD} doctor 2>&1")
    
    if "Config invalid" in out or "Unrecognized key" in out:
        print("   ⚠️ 发现配置错误，修复中...")
        code, out, err = run_cmd(f"{OPENCLAW_CMD} doctor --fix 2>&1")
        if "Config invalid" not in out:
            print("   ✅ 配置已修复")
            return False
    
    print("   ✅ 配置正常")
    return True

def check_port():
    """检查端口"""
    print("🔍 检查 Gateway 响应...")
    code, out, err = run_cmd("curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:18789/")
    
    if code == 0 and out in ["200", "301", "302"]:
        print("   ✅ Gateway 响应正常")
        return True
    else:
        print("   ⚠️ Gateway 可能异常")
        return False

def fix_all():
    """修复所有问题"""
    print("="*50)
    print("🚨 紧急检查与修复")
    print("="*50)
    
    issues = []
    
    # 1. 检查配置
    if not check_config():
        issues.append("配置错误")
    
    # 2. 检查Gateway
    if not check_gateway():
        issues.append("Gateway重启")
    
    # 3. 检查端口
    if not check_port():
        issues.append("端口异常")
    
    # 最终状态
    print("\n" + "="*50)
    if not issues:
        print("✅ 所有检查通过！无问题发现。")
    else:
        print(f"⚠️ 发现 {len(issues)} 个问题，已尝试修复")
        for issue in issues:
            print(f"   - {issue}")
    print("="*50)
    
    return len(issues) == 0

if __name__ == "__main__":
    fix_all()

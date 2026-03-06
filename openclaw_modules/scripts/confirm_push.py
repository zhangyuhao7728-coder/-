#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
推送项目到GitHub
需确认后执行
"""

import os
import subprocess
from datetime import datetime

PROJECT_PATH = "/Users/zhangyuhao/项目/Ai学习系统"

def run_cmd(cmd, cwd=None):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    return result.returncode, result.stdout, result.stderr

def check_pending_push():
    """检查是否有待推送的提交"""
    os.chdir(PROJECT_PATH)
    returncode, stdout, _ = run_cmd("git log origin/main..HEAD --oneline")
    return returncode == 0 and stdout.strip() != ""

def push():
    """推送"""
    os.chdir(PROJECT_PATH)
    
    # 检查
    if not check_pending_push():
        return False, "没有待推送的提交"
    
    # 推送
    returncode, stdout, stderr = run_cmd("git push origin main")
    
    if returncode != 0:
        return False, f"推送失败: {stderr}"
    
    return True, "推送成功!"

def main():
    print("\n🚀 推送到GitHub")
    print("="*50)
    
    success, msg = push()
    
    if success:
        print(f"✅ {msg}")
    else:
        print(f"❌ {msg}")
    
    return success

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)

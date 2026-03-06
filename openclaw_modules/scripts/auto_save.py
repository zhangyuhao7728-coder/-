#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动保存项目到GitHub
检测变更并自动提交，Push需确认
"""

import os
import subprocess
import sys
from datetime import datetime

# 项目路径
PROJECT_PATH = "/Users/zhangyuhao/项目/Ai学习系统"
GIT_REMOTE = "origin"
GIT_BRANCH = "main"

def run_cmd(cmd, cwd=None):
    """运行命令"""
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True, cwd=cwd
    )
    return result.returncode, result.stdout, result.stderr

def check_git_installed():
    """检查git是否安装"""
    return run_cmd("which git")[0] == 0

def check_github_connected():
    """检查GitHub连接"""
    returncode, stdout, _ = run_cmd("gh auth status")
    print(f"Debug: {stdout}")  # Debug
    return returncode == 0 and "github.com" in stdout

def get_changes():
    """获取变更状态"""
    os.chdir(PROJECT_PATH)
    returncode, stdout, _ = run_cmd("git status --porcelain")
    return stdout.strip() if returncode == 0 else ""

def commit_changes(message=None):
    """提交变更"""
    os.chdir(PROJECT_PATH)
    
    if not message:
        message = f"Auto backup: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    
    # git add
    returncode, _, stderr = run_cmd("git add -A")
    if returncode != 0:
        return False, f"git add failed: {stderr}"
    
    # git commit
    returncode, stdout, stderr = run_cmd(f'git commit -m "{message}"')
    if returncode != 0:
        if "nothing to commit" in stderr:
            return True, "没有变更需要提交"
        return False, f"git commit failed: {stderr}"
    
    return True, stdout.strip()

def push_to_github():
    """推送到GitHub"""
    os.chdir(PROJECT_PATH)
    returncode, stdout, stderr = run_cmd(f"git push {GIT_REMOTE} {GIT_BRANCH}")
    
    if returncode != 0:
        return False, f"Push failed: {stderr}"
    
    return True, stdout.strip()

def auto_save():
    """自动保存"""
    print(f"\n🔄 项目自动保存")
    print("="*50)
    print(f"项目: {PROJECT_PATH}")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50)
    
    # 检查变更
    changes = get_changes()
    
    if not changes:
        print("✅ 没有变更")
        return True, "无变更"
    
    # 显示变更文件数
    files = changes.split('\n')
    print(f"📝 发现 {len(files)} 个文件变更")
    
    # 提交
    success, msg = commit_changes()
    if not success:
        return False, msg
    
    print(f"✅ 已提交: {msg}")
    
    # 返回待推送状态
    return True, f"已提交 {len(files)} 个文件变更，等待推送"

def main():
    if not check_git_installed():
        print("❌ Git未安装")
        sys.exit(1)
    
    if not check_github_connected():
        print("❌ GitHub未连接")
        sys.exit(1)
    
    success, msg = auto_save()
    print(msg)
    
    if "等待推送" in msg:
        print("\n💡 提示: 输入 '确认推送' 命令来推送到GitHub")

if __name__ == "__main__":
    main()

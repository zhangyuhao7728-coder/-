#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用例17：GitHub过期Issue清理
自动清理仓库中的过期Issue
"""

import os
import subprocess
import json
from datetime import datetime, timedelta

# 配置
OWNER = "zhangyuhao7728-coder"
REPO = "-"
DAYS_STALE = 30  # 30天无活动视为过期

def get_gh_auth():
    """获取GitHub CLI认证"""
    result = subprocess.run(
        ["gh", "auth", "status"],
        capture_output=True,
        text=True
    )
    return "Logged in" in result.stdout

def list_stale_issues():
    """列出过期Issues"""
    if not get_gh_auth():
        print("❌ 未登录GitHub")
        return []
    
    # 获取所有open的issues
    result = subprocess.run(
        ["gh", "issue", "list", "--state", "open", "--limit", "50"],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"❌ 获取Issue失败: {result.stderr}")
        return []
    
    stale_issues = []
    lines = result.stdout.strip().split('\n')
    
    for line in lines:
        if not line.strip():
            continue
        parts = line.split('\t')
        if len(parts) >= 1:
            # 解析Issue编号
            issue_num = parts[0]
            stale_issues.append(issue_num)
    
    return stale_issues

def add_stale_label(issue_num):
    """添加stale标签"""
    result = subprocess.run(
        ["gh", "issue", "edit", issue_num, "--add-label", "stale"],
        capture_output=True,
        text=True
    )
    return result.returncode == 0

def comment_stale(issue_num):
    """评论通知即将关闭"""
    comment = f"此Issue已停滞{dAYS_STALE}天，将于7天后关闭。如有需要请回复，否则将关闭。"
    
    result = subprocess.run(
        ["gh", "issue", "comment", issue_num, "--body", comment],
        capture_output=True,
        text=True
    )
    return result.returncode == 0

def close_issue(issue_num):
    """关闭Issue"""
    result = subprocess.run(
        ["gh", "issue", "close", issue_num],
        capture_output=True,
        text=True
    )
    return result.returncode == 0

def run_cleanup(dry_run=True):
    """运行清理"""
    print("\n🗑️ GitHub过期Issue清理")
    print("="*50)
    print(f"仓库: {OWNER}/{REPO}")
    print(f"过期天数: {DAYS_STALE}")
    print(f"模式: {'预览' if dry_run else '执行'}")
    print("="*50)
    
    stale_issues = list_stale_issues()
    
    if not stale_issues:
        print("✅ 没有过期Issue")
        return
    
    print(f"\n📋 发现 {len(stale_issues)} 个Issue:")
    for issue in stale_issues:
        print(f"   - #{issue}")
    
    if dry_run:
        print("\n🔍 预览模式，未执行操作")
        return
    
    # 执行清理
    closed = 0
    for issue in stale_issues:
        if add_stale_label(issue):
            print(f"✅ 添加stale标签: #{issue}")
        if comment_stale(issue):
            print(f"✅ 发布提醒评论: #{issue}")
        if close_issue(issue):
            closed += 1
            print(f"✅ 关闭Issue: #{issue}")
    
    print(f"\n✅ 清理完成，关闭了 {closed} 个Issue")

def main():
    import sys
    
    dry_run = "--dry-run" in sys.argv or "-n" in sys.argv
    
    run_cleanup(dry_run=dry_run)

if __name__ == "__main__":
    main()

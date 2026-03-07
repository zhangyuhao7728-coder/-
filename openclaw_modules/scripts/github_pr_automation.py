#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用例27：GitHub Pull Request自动化
自动审查和管理PR
"""

import subprocess
import json
from datetime import datetime

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

def list_prs():
    """列出PR"""
    code, out, err = run_cmd("gh pr list --limit 10 --json number,title,state,author,createdAt")
    
    if code != 0:
        return []
    
    try:
        return json.loads(out)
    except:
        return []

def get_pr_reviews(pr_num):
    """获取PR审查"""
    code, out, err = run_cmd(f"gh pr view {pr_num} --json reviews")
    
    if code != 0:
        return []
    
    try:
        data = json.loads(out)
        return data.get("reviews", [])
    except:
        return []

def check_pr_ready(pr):
    """检查PR是否准备好合并"""
    pr_num = pr["number"]
    reviews = get_pr_reviews(pr_num)
    
    # 检查是否有批准
    approved = any(r.get("state") == "APPROVED" for r in reviews)
    
    # 检查是否有评论需要回复
    has_comments = len(reviews) > 0
    
    return {
        "approved": approved,
        "has_reviews": has_comments,
        "ready": approved and not has_comments
    }

def generate_report():
    """生成报告"""
    print("="*50)
    print("🔀 GitHub Pull Request 自动化")
    print("="*50)
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    prs = list_prs()
    
    if not prs:
        print("\n✅ 没有待处理的PR")
        return
    
    print(f"\n📋 待处理PR: {len(prs)} 个")
    
    ready_to_merge = []
    needs_review = []
    
    for pr in prs:
        check = check_pr_ready(pr)
        
        if check["ready"]:
            ready_to_merge.append(pr)
        else:
            needs_review.append(pr)
        
        status = "✅ 可合并" if check["ready"] else "📝 需要审查"
        
        print(f"\n  #{pr['number']} {pr['title'][:40]}")
        print(f"     作者: {pr.get('author', 'unknown')}")
        print(f"     状态: {status}")
    
    # 总结
    print("\n" + "="*50)
    print(f"\n📊 总结:")
    print(f"   ✅ 可合并: {len(ready_to_merge)}")
    print(f"   📝 需要审查: {len(needs_review)}")
    
    if ready_to_merge:
        pr_num = ready_to_merge[0]["number"]
        print(f"\n💡 可用 '合并PR #{pr_num}' 合并")

def merge_pr(pr_num):
    """合并PR"""
    code, out, err = run_cmd(f"gh pr merge {pr_num} --admin --squash")
    
    if code == 0:
        print(f"✅ PR #{pr_num} 已合并")
        return True
    else:
        print(f"❌ 合并失败: {err}")
        return False

def main():
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "merge" and len(sys.argv) > 2:
            merge_pr(sys.argv[2])
        else:
            print("用法:")
            print("  python github_pr_automation.py          # 查看PR状态")
            print("  python github_pr_automation.py merge 1  # 合并PR #1")
    else:
        generate_report()

if __name__ == "__main__":
    main()

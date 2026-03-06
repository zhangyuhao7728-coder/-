#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用例07：GitHub Issue优先级排序
按优先级给Issue排序，标记重要Issue
"""

import os
import subprocess
import json
from datetime import datetime, timedelta

# 配置
OWNER = "zhangyuhao7728-coder"
REPO = "-"
DAYS_UNRESPONSIVE = 7  # 7天无响应视为过期
DAYS_URGENT = 3        # 3天无响应标记紧急

# 关键词权重
SECURITY_KEYWORDS = ["security", "安全", "vulnerability", "漏洞", "exploit"]
CRASH_KEYWORDS = ["crash", "崩溃", "bug", "错误", "fatal", "critical"]
URGENT_KEYWORDS = ["urgent", "紧急", "important", "asap", "help wanted"]

def get_issues():
    """获取所有open的issues"""
    result = subprocess.run(
        ["gh", "issue", "list", "--state", "open", "--limit", "100", "--json", "number,title,labels,createdAt,comments"],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        return []
    
    try:
        return json.loads(result.stdout)
    except:
        return []

def calculate_priority(issue):
    """计算优先级分数"""
    score = 0
    title = issue.get("title", "").lower()
    labels = [l.lower() for l in issue.get("labels", [])]
    
    # 1. 关键词检测
    if any(k in title for k in SECURITY_KEYWORDS):
        score += 100
    if any(k in title for k in CRASH_KEYWORDS):
        score += 80
    if any(k in title for k in URGENT_KEYWORDS):
        score += 50
    
    # 2. 标签权重
    priority_labels = ["priority:high", "urgent", "critical", "bug", "security", "important"]
    if any(l in labels for l in priority_labels):
        score += 60
    
    # 3. 评论数（用户关注度）
    comments = issue.get("comments", 0)
    score += comments * 5
    
    # 4. 时间紧迫性
    created = datetime.fromisoformat(issue.get("createdAt", "").replace("Z", "+00:00"))
    days_old = (datetime.now() - created.replace(tzinfo=None)).days
    
    if days_old > DAYS_UNRESPONSIVE:
        score += 30
    if days_old > DAYS_URGENT:
        score += 20
    
    return score, days_old

def sort_issues(issues):
    """排序issues"""
    scored = []
    
    for issue in issues:
        score, days = calculate_priority(issue)
        scored.append({
            "number": issue.get("number"),
            "title": issue.get("title"),
            "score": score,
            "days_old": days,
            "comments": issue.get("comments", 0),
            "labels": issue.get("labels", [])
        })
    
    # 按分数降序
    return sorted(scored, key=lambda x: x["score"], reverse=True)

def generate_report(sorted_issues):
    """生成报告"""
    print("\n📊 GitHub Issue 优先级报告")
    print("="*50)
    print(f"仓库: {OWNER}/{REPO}")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*50)
    
    if not sorted_issues:
        print("✅ 没有open的Issue")
        return
    
    # 分类
    high_priority = [i for i in sorted_issues if i["score"] >= 50]
    medium_priority = [i for i in sorted_issues if 20 <= i["score"] < 50]
    low_priority = [i for i in sorted_issues if i["score"] < 20]
    
    print(f"\n📈 统计: 共 {len(sorted_issues)} 个Issue")
    print(f"   🔴 高优先级: {len(high_priority)}")
    print(f"   🟡 中优先级: {len(medium_priority)}")
    print(f"   🟢 低优先级: {len(low_priority)}")
    
    # 高优先级详情
    if high_priority:
        print(f"\n🔴 高优先级 (Top 10):")
        for i, issue in enumerate(high_priority[:10], 1):
            print(f"   {i}. #{issue['number']} - {issue['title'][:50]}")
            print(f"      分数: {issue['score']} | {issue['days_old']}天 | {issue['comments']}评论")
    
    # 过期Issue
    stale = [i for i in sorted_issues if i["days_old"] > DAYS_UNRESPONSIVE]
    if stale:
        print(f"\n⚠️ 过期Issue ({DAYS_UNRESPONSIVE}+天):")
        for issue in stale[:5]:
            print(f"   #{issue['number']} - {issue['title'][:40]}")
    
    return len(high_priority) > 0

def main():
    issues = get_issues()
    sorted_issues = sort_issues(issues)
    generate_report(sorted_issues)

if __name__ == "__main__":
    main()

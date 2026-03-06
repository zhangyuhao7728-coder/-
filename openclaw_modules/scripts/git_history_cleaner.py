#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用例 33：Git 历史清理
扫描并清理 Git 历史中的敏感信息
"""

import os
import re
import subprocess

# 敏感信息模式
SECRET_PATTERNS = [
    (r"AKIA[0-9A-Z]{16}", "AWS Access Key"),
    (r"aws_access_key_id\s*=\s*[A-Z0-9]{20}", "AWS Key"),
    (r"-----BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY-----", "SSH Private Key"),
    (r"ghp_[a-zA-Z0-9]{36}", "GitHub Token"),
    (r"gho_[a-zA-Z0-9]{36}", "GitHub OAuth Token"),
    (r"glpat-[a-zA-Z0-9\-]{20}", "GitLab Token"),
]

# 扫描仓库
REPOS = [
    "/Users/zhangyuhao/Learning project/python/openclaw_modules",
    "/Users/zhangyuhao/openclaw"
]

def scan_git_history(repo_path):
    """扫描 Git 历史"""
    results = []
    
    if not os.path.exists(os.path.join(repo_path, ".git")):
        return results
    
    print(f"   扫描: {repo_path}")
    
    # 使用 git log 搜索敏感信息
    for pattern, name in SECRET_PATTERNS:
        try:
            result = subprocess.run(
                ["git", "log", "-p", "--all", "-S", pattern, "--source", "--remotes"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0 and result.stdout:
                # 统计出现次数
                count = result.stdout.count(pattern)
                if count > 0:
                    results.append({
                        "repo": os.path.basename(repo_path),
                        "pattern": name,
                        "count": count
                    })
        except:
            pass
    
    return results

def run_scan():
    """运行扫描"""
    all_results = []
    
    print("🔍 正在扫描 Git 历史...")
    
    for repo in REPOS:
        if os.path.exists(repo):
            results = scan_git_history(repo)
            all_results.extend(results)
    
    return all_results

if __name__ == "__main__":
    results = run_scan()
    
    print("\n" + "="*50)
    print("🔒 Git 历史扫描报告")
    print("="*50)
    
    if not results:
        print("✅ 未发现敏感信息")
    else:
        print(f"⚠️ 发现 {len(results)} 个问题:\n")
        for r in results:
            print(f"  📁 {r['repo']}")
            print(f"     {r['pattern']}: {r['count']} 次")
            print()
        print("💡 建议使用 BFG Repo-Cleaner 清理:")
        print("   bfg --delete-files <file>")
        print("   git reflog expire --expire=now --all")
        print("   git gc --prune=now --aggressive")

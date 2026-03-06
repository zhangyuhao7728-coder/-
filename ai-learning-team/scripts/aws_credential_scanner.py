#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用例 29：AWS 凭证扫描器
检查 AWS 密钥泄露
"""

import os
import re
import subprocess
from pathlib import Path

# AWS 密钥模式
AWS_PATTERNS = [
    r"AKIA[0-9A-Z]{16}",  # Access Key ID
    r"aws_access_key_id\s*=\s*[A-Z0-9]{20}",
    r"aws_secret_access_key\s*=\s*[A-Za-z0-9/+=]{40}",
]

# 扫描路径
SCAN_PATHS = [
    os.path.expanduser("~"),
    "/Users/zhangyuhao/Learning project/python/ai-learning-team",
    "/Users/zhangyuhao/openclaw"
]

def scan_file(filepath):
    """扫描文件内容"""
    try:
        with open(filepath, 'r', errors='ignore') as f:
            content = f.read(8192)
            for pattern in AWS_PATTERNS:
                if re.search(pattern, content):
                    return True
    except:
        pass
    return False

def scan_directory(base_path):
    """扫描目录"""
    results = []
    
    for root, dirs, files in os.walk(base_path):
        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', '.venv']]
        
        for file in files:
            filepath = os.path.join(root, file)
            
            # 只扫描可能包含密钥的文件
            if file.endswith(('.py', '.sh', '.json', '.yml', '.yaml', '.env', '.txt', '.conf', '.config')):
                if scan_file(filepath):
                    results.append({
                        "file": filepath,
                        "issue": "包含 AWS 密钥",
                        "severity": "🔴 高"
                    })
    
    return results

def run_scan():
    """运行扫描"""
    all_results = []
    
    print("🔍 正在扫描 AWS 凭证...")
    
    for path in SCAN_PATHS:
        if os.path.exists(path):
            print(f"   扫描: {path}")
            results = scan_directory(path)
            all_results.extend(results)
    
    return all_results

if __name__ == "__main__":
    results = run_scan()
    
    print("\n" + "="*50)
    print("🔒 AWS 凭证扫描报告")
    print("="*50)
    
    if not results:
        print("✅ 未发现 AWS 密钥泄露")
    else:
        print(f"⚠️ 发现 {len(results)} 个问题:\n")
        for r in results:
            print(f"  {r['severity']} {r['file']}")
            print(f"     问题: {r['issue']}")
            print()

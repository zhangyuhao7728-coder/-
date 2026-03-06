#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用例 09：SSH 私钥扫描器
检查密钥泄露风险
"""

import os
import re
import subprocess
from pathlib import Path

# 扫描路径
SCAN_PATHS = [
    os.path.expanduser("~"),
    "/Users/zhangyuhao/Learning project/python/ai-learning-team",
    "/Users/zhangyuhao/openclaw"
]

# SSH 私钥文件名模式
SSH_KEY_PATTERNS = [
    r"id_rsa",
    r"id_dsa",
    r"id_ecdsa",
    r"id_ed25519",
    r"\.pem",
    r"\.key",
    r"\.ppk"
]

# 危险内容模式
DANGEROUS_PATTERNS = [
    r"-----BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY-----",
    r"-----BEGIN CERTIFICATE-----",
    r"aws_access_key",
    r"aws_secret_key",
    r"AKIA[0-9A-Z]{16}"
]

def scan_file(filepath):
    """扫描文件内容"""
    try:
        with open(filepath, 'r', errors='ignore') as f:
            content = f.read(8192)  # 只读前8KB
            for pattern in DANGEROUS_PATTERNS:
                if re.search(pattern, content):
                    return True
    except:
        pass
    return False

def check_permissions(filepath):
    """检查文件权限"""
    try:
        stat = os.stat(filepath)
        mode = stat.st_mode & 0o777
        # 644 或更宽松的权限是危险的
        if mode > 0o600:
            return False
        return True
    except:
        return False

def scan_directory(base_path):
    """扫描目录"""
    results = []
    
    for root, dirs, files in os.walk(base_path):
        # 跳过某些目录
        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__']]
        
        for file in files:
            filepath = os.path.join(root, file)
            
            # 检查文件名
            for pattern in SSH_KEY_PATTERNS:
                if re.search(pattern, file, re.IGNORECASE):
                    # 检查权限
                    perm_ok = check_permissions(filepath)
                    # 检查内容
                    has_secret = scan_file(filepath)
                    
                    if not perm_ok or has_secret:
                        results.append({
                            "file": filepath,
                            "issue": "权限过宽" if not perm_ok else "包含密钥",
                            "severity": "🔴 高" if has_secret else "🟡 中"
                        })
    
    return results

def run_scan():
    """运行扫描"""
    all_results = []
    
    print("🔍 正在扫描 SSH 私钥...")
    
    for path in SCAN_PATHS:
        if os.path.exists(path):
            print(f"   扫描: {path}")
            results = scan_directory(path)
            all_results.extend(results)
    
    return all_results

if __name__ == "__main__":
    results = run_scan()
    
    print("\n" + "="*50)
    print("🔒 SSH 私钥扫描报告")
    print("="*50)
    
    if not results:
        print("✅ 未发现安全问题")
    else:
        print(f"⚠️ 发现 {len(results)} 个问题:\n")
        for r in results:
            print(f"  {r['severity']} {r['file']}")
            print(f"     问题: {r['issue']}")
            print()

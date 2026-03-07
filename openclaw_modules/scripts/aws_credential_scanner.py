#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AWS凭证扫描 - 优化版
快速检测AWS凭据泄露
"""

import os
import subprocess
from datetime import datetime

def check_aws_credentials():
    """检查AWS凭据"""
    print("☁️ AWS凭证快速扫描")
    print("="*50)
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*50)
    
    results = []
    
    # 1. 检查环境变量
    print("\n1️⃣ 检查环境变量...")
    aws_keys = ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN"]
    found = []
    for key in aws_keys:
        if os.environ.get(key):
            found.append(key)
    
    if found:
        print(f"   ⚠️ 发现环境变量: {', '.join(found)}")
        results.append(("环境变量", False))
    else:
        print("   ✅ 无AWS环境变量")
        results.append(("环境变量", True))
    
    # 2. 检查AWS CLI配置
    print("\n2️⃣ 检查AWS CLI配置...")
    aws_dir = os.path.expanduser("~/.aws")
    if os.path.exists(aws_dir):
        files = os.listdir(aws_dir)
        print(f"   📁 AWS目录存在: {files}")
        
        # 检查敏感文件
        creds_file = os.path.join(aws_dir, "credentials")
        if os.path.exists(creds_file):
            print("   ⚠️ 发现credentials文件")
            results.append(("CLI配置", False))
        else:
            print("   ✅ 无credentials文件")
            results.append(("CLI配置", True))
    else:
        print("   ✅ 无AWS CLI配置")
        results.append(("CLI配置", True))
    
    # 3. 检查常见泄露位置
    print("\n3️⃣ 检查常见泄露位置...")
    dangerous_paths = [
        "~/.aws/credentials",
        "~/aws.pem",
        "~/aws-key.pem",
    ]
    
    leaks = []
    for path in dangerous_paths:
        full_path = os.path.expanduser(path)
        if os.path.exists(full_path):
            leaks.append(path)
    
    if leaks:
        print(f"   ❌ 发现可疑文件: {leaks}")
        results.append(("泄露检测", False))
    else:
        print("   ✅ 未发现泄露")
        results.append(("泄露检测", True))
    
    # 总结
    print("\n" + "="*50)
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    print(f"\n📊 检查结果: {passed}/{total} 通过")
    
    if passed == total:
        print("   ✅ 未发现AWS凭证泄露风险")
    else:
        print("   ⚠️ 建议检查以上问题")
    
    return passed == total

if __name__ == "__main__":
    check_aws_credentials()

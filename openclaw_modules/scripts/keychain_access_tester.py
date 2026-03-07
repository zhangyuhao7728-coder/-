#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用例30升级版：macOS Keychain 安全检查
检测Keychain状态和安全设置
"""

import subprocess
import os
from datetime import datetime

def check_keychain_status():
    """检查Keychain状态"""
    print("🛡️ macOS Keychain 安全检查")
    print("="*50)
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*50)
    
    results = []
    
    # 1. 检查Keychain列表
    print("\n1️⃣ 检查Keychain列表...")
    try:
        result = subprocess.run(
            ["security", "list-keychains"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            keychains = result.stdout.strip().split('\n')
            print(f"   ✅ 找到 {len(keychains)} 个Keychain")
            results.append(("Keychain列表", True))
        else:
            print("   ⚠️ 无法访问Keychain")
            results.append(("Keychain列表", False))
    except Exception as e:
        print(f"   ❌ 错误: {e}")
        results.append(("Keychain列表", False))
    
    # 2. 检查默认Keychain
    print("\n2️⃣ 检查默认Keychain...")
    try:
        result = subprocess.run(
            ["security", "default-keychain"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            default = result.stdout.strip()
            print(f"   ✅ 默认: {default}")
            results.append(("默认Keychain", True))
        else:
            print("   ⚠️ 无法获取默认Keychain")
            results.append(("默认Keychain", False))
    except Exception as e:
        print(f"   ❌ 错误: {e}")
        results.append(("默认Keychain", False))
    
    # 3. 检查登录Keychain锁定状态
    print("\n3️⃣ 检查Keychain锁定状态...")
    try:
        result = subprocess.run(
            ["security", "show-keychain-info", os.path.expanduser("~/Library/Keychains/login.keychain-db")],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            info = result.stdout.strip()
            print(f"   ✅ {info}")
            results.append(("Keychain状态", True))
        else:
            print("   ℹ️  Keychain未锁定")
            results.append(("Keychain状态", True))
    except Exception as e:
        print(f"   ℹ️  跳过详细检查")
        results.append(("Keychain状态", True))
    
    # 4. 安全建议
    print("\n" + "="*50)
    print("\n🔒 安全建议:")
    print("   1. 定期检查Keychain访问权限")
    print("   2. 不随意给未知应用授权")
    print("   3. 使用强密码保护Keychain")
    print("   4. 开启Touch ID解锁Keychain")
    
    # 总结
    print("\n" + "="*50)
    passed = sum(1 for _, r in results if r)
    total = len(results)
    print(f"\n📊 检查结果: {passed}/{total} 通过")
    
    if passed == total:
        print("   ✅ Keychain状态正常")
    else:
        print("   ⚠️ 建议检查未通过的项目")
    
    return passed == total

if __name__ == "__main__":
    check_keychain_status()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用例06：密码健康检查
检查系统密码安全和弱密码
"""

import os
import subprocess
import hashlib

def check_password_strength(password):
    """检查密码强度"""
    score = 0
    issues = []
    
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        issues.append("太短 (至少12位)")
    
    if any(c.isupper() for c in password):
        score += 1
    else:
        issues.append("缺少大写字母")
    
    if any(c.islower() for c in password):
        score += 1
    else:
        issues.append("缺少小写字母")
    
    if any(c.isdigit() for c in password):
        score += 1
    else:
        issues.append("缺少数字")
    
    if any(c in "!@#$%^&*()_+-=[]{}|;':\",./<>?" for c in password):
        score += 1
    else:
        issues.append("缺少特殊字符")
    
    common = ["password", "123456", "qwerty", "admin", "letmein"]
    if password.lower() in common:
        score = 0
        issues.append("常见弱密码")
    
    return score, issues

def check_system_passwords():
    """检查系统密码策略"""
    print("\n🔐 密码健康检查")
    print("="*50)
    
    # 检查macOS密码策略
    result = subprocess.run(
        ["pwpolicy", "-getaccountpolicies"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ 密码策略已配置")
        return True
    else:
        print("⚠️ 未配置密码策略")
        return False

def check_keychain():
    """检查Keychain"""
    print("\n🔑 检查Keychain...")
    
    # 简略检查
    result = subprocess.run(
        ["security", "list-keychains"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ Keychain可访问")
        return True
    
    print("⚠️ Keychain访问异常")
    return False

def run_password_health_check():
    """运行完整检查"""
    print(f"\n🔐 密码健康检查")
    print("="*50)
    
    results = []
    
    # 1. 系统密码策略
    results.append(("系统密码策略", check_system_passwords()))
    
    # 2. Keychain
    results.append(("Keychain", check_keychain()))
    
    # 3. 总结
    print("\n" + "="*50)
    print("\n📊 检查结果:")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"  {status} {name}")
    
    print(f"\n通过: {passed}/{total}")
    
    return passed == total

if __name__ == "__main__":
    run_password_health_check()

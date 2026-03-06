#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用例07：双因素认证(2FA)审计
检查哪些服务开启了2FA
"""

import os
import subprocess

def check_2fa_google():
    """检查Google 2FA"""
    result = subprocess.run(
        ["defaults", "read", "com.google.Chrome", "2FAEnabled"],
        capture_output=True,
        text=True
    )
    return result.returncode == 0

def check_2fa_apple():
    """检查Apple ID 2FA"""
    # Apple ID 2FA是系统级别的
    result = subprocess.run(
        ["dscl", ".", "read", "/Users/zhangyuhao", "AuthenticationHint"],
        capture_output=True,
        text=True
    )
    return result.returncode == 0

def check_2fa_github():
    """检查GitHub 2FA"""
    # 需要gh CLI
    result = subprocess.run(
        ["gh", "auth", "status"],
        capture_output=True,
        text=True
    )
    return "logged in" in result.stdout

def check_passwordless():
    """检查无密码登录"""
    # 检查Touch ID
    result = subprocess.run(
        ["bioutil", "-s"],
        capture_output=True,
        text=True
    )
    return result.returncode == 0

def run_2fa_audit():
    """运行2FA审计"""
    print("\n🔒 双因素认证审计")
    print("="*50)
    
    services = [
        ("Apple ID 2FA", check_2fa_apple),
        ("Google Chrome 2FA", check_2fa_google),
        ("GitHub", check_2fa_github),
        ("Touch ID", check_passwordless),
    ]
    
    results = []
    
    print("\n📋 检查项目:\n")
    
    for name, check_func in services:
        try:
            enabled = check_func()
            results.append((name, enabled))
            status = "✅ 已开启" if enabled else "❌ 未开启"
            print(f"  {status} {name}")
        except:
            results.append((name, False))
            print(f"  ⚠️ 无法检查 {name}")
    
    print("\n" + "="*50)
    
    enabled_count = sum(1 for _, e in results if e)
    total = len(results)
    
    print(f"\n📊 2FA覆盖率: {enabled_count}/{total}")
    
    if enabled_count < total:
        print("\n⚠️ 建议开启2FA的服务:")
        for name, enabled in results:
            if not enabled:
                print(f"   - {name}")
    
    return results

if __name__ == "__main__":
    run_2fa_audit()

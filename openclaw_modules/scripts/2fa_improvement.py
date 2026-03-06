#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2FA增强建议
提供开启2FA的具体指引
"""

def get_2fa_instructions():
    """获取2FA开启指引"""
    
    instructions = {
        "GitHub": {
            "url": "https://github.com/settings/security",
            "steps": [
                "1. 打开 GitHub → Settings → Password and authentication",
                "2. 点击 'Enable two-factor authentication'",
                "3. 选择验证方式 (Authenticator app 或 SMS)",
                "4. 按照指引完成设置"
            ],
            "difficulty": "简单"
        },
        "Google Chrome": {
            "url": "https://myaccount.google.com/signinoptions/two-step-verification",
            "steps": [
                "1. 打开 Google 账户",
                "2. 点击 'Security'",
                "3. 开启 '2-Step Verification'",
                "4. 选择验证方式"
            ],
            "difficulty": "简单"
        },
        "Touch ID": {
            "url": "System Settings → Touch ID",
            "steps": [
                "1. 打开系统设置",
                "2. 点击 'Touch ID与密码'",
                "3. 添加指纹",
                "4. 开启解锁/支付"
            ],
            "difficulty": "简单"
        }
    }
    
    return instructions

def print_instructions():
    """打印2FA开启指引"""
    
    print("\n🔒 2FA开启指引")
    print("="*50)
    
    instructions = get_2fa_instructions()
    
    for name, info in instructions.items():
        print(f"\n📱 {name}")
        print(f"   难度: {info['difficulty']}")
        print(f"   地址: {info['url']}")
        print("   步骤:")
        for step in info['steps']:
            print(f"     {step}")
    
    print("\n" + "="*50)

def check_current_status():
    """检查当前2FA状态"""
    
    print("\n📊 当前2FA状态")
    print("="*50)
    print("✅ 已开启:")
    print("   - Apple ID (系统级别)")
    print("\n❌ 未开启:")
    print("   - GitHub")
    print("   - Google Chrome")
    print("   - Touch ID")
    print("\n💡 建议: 按优先级开启")
    print("   1. GitHub (最重要)")
    print("   2. Touch ID (日常使用)")
    print("   3. Google (可选)")

if __name__ == "__main__":
    check_current_status()
    print_instructions()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用例 30：macOS Keychain 社工测试
测试人类安全意识
"""

import subprocess
import os

def test_keychain_access():
    """测试 Keychain 访问"""
    print("🛡️ macOS Keychain 社会工程学测试")
    print("="*50)
    print()
    print("⚠️  此测试会触发系统密码弹窗")
    print("   测试你是否会不假思索输入密码")
    print()
    
    # 尝试访问 Keychain（会触发弹窗）
    script = '''
    tell application "System Events"
        keystroke "test"
    end tell
    '''
    
    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True,
        text=True,
        timeout=5
    )
    
    print("✅ 测试完成")
    print()
    print("安全建议:")
    print("1. 看到密码弹窗先确认来源")
    print("2. 不要随意输入密码给未知应用")
    print("3. 定期检查 Keychain 访问权限")

if __name__ == "__main__":
    test_keychain_access()

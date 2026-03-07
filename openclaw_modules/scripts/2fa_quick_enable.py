#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2FA一键优化 - 静默版
"""

import subprocess
import os

def open_url(url):
    subprocess.run(["open", url])

# GitHub已打开
print("🔐 正在打开GitHub 2FA设置...")
open_url("https://github.com/settings/security")

print("""
==================================================
🔐 2FA一键优化

📋 当前状态:
   ✅ Apple ID 2FA
   ❌ GitHub 2FA
   ❌ Touch ID
   ❌ Google 2FA

已在浏览器打开 GitHub 安全设置

请完成以下步骤:
1. 点击 "Enable two-factor authentication"
2. 选择 "Authenticator app" (推荐)
3. 扫描二维码
4. 保存备份码

完成后告诉我验证！
==================================================
""")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用例05：SSH密钥自动轮换
定期自动更换SSH密钥
"""

import os
import subprocess
import shutil
from datetime import datetime, timedelta

BACKUP_DIR = os.path.expanduser("~/.ssh/backups")
ROTATE_DAYS = 90  # 90天轮换

def backup_key(key_path):
    """备份现有密钥"""
    if not os.path.exists(key_path):
        return False
    
    os.makedirs(BACKUP_DIR, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d")
    backup_path = os.path.join(BACKUP_DIR, f"ssh_key_{timestamp}")
    
    shutil.copy2(key_path, backup_path)
    shutil.copy2(key_path + ".pub", backup_path + ".pub")
    
    return True

def generate_new_key(key_path):
    """生成新SSH密钥"""
    if os.path.exists(key_path):
        print(f"⚠️ 密钥已存在: {key_path}")
        return False
    
    result = subprocess.run(
        ["ssh-keygen", "-t", "ed25519", "-f", key_path, "-N", "", "-C", "openclaw@automation"],
        capture_output=True,
        text=True
    )
    
    return result.returncode == 0

def check_key_age(key_path):
    """检查密钥年龄"""
    if not os.path.exists(key_path):
        return None
    
    mtime = os.path.getmtime(key_path)
    age_days = (datetime.now() - datetime.fromtimestamp(mtime)).days
    
    return age_days

def add_to_authorized_keys(key_path):
    """添加公钥到authorized_keys"""
    pub_path = key_path + ".pub"
    
    if not os.path.exists(pub_path):
        return False
    
    with open(pub_path, 'r') as f:
        pub_key = f.read().strip()
    
    auth_keys = os.path.expanduser("~/.ssh/authorized_keys")
    
    with open(auth_keys, 'a') as f:
        f.write(f"\n{pub_key}\n")
    
    return True

def rotate_ssh_key(key_path="~/.ssh/id_ed25519"):
    """轮换SSH密钥"""
    key_path = os.path.expanduser(key_path)
    
    print(f"\n🔑 SSH密钥自动轮换")
    print("="*50)
    
    # 检查密钥年龄
    age = check_key_age(key_path)
    
    if age is None:
        print("❌ 密钥不存在")
        return False
    
    print(f"📅 当前密钥年龄: {age}天")
    
    if age < ROTATE_DAYS:
        print(f"✅ 密钥还可使用 ({ROTATE_DAYS - age}天后轮换)")
        return True
    
    # 轮换
    print("\n🔄 开始轮换...")
    
    # 1. 备份旧密钥
    if backup_key(key_path):
        print("✅ 旧密钥已备份")
    
    # 2. 生成新密钥
    if generate_new_key(key_path):
        print("✅ 新密钥已生成")
    else:
        print("❌ 生成新密钥失败")
        return False
    
    # 3. 添加到authorized_keys
    if add_to_authorized_keys(key_path):
        print("✅ 公钥已添加")
    
    print("\n✅ 密钥轮换完成!")
    return True

def main():
    import sys
    
    key_path = sys.argv[1] if len(sys.argv) > 1 else "~/.ssh/id_ed25519"
    
    rotate_ssh_key(key_path)

if __name__ == "__main__":
    main()

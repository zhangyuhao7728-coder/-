#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSH密钥扫描 - 优化版
快速检测SSH密钥
"""

import os
import subprocess
from datetime import datetime

def check_ssh_key(path):
    """检查单个SSH密钥"""
    if not os.path.exists(path):
        return None
    
    stat = os.stat(path)
    return {
        "path": path,
        "size": stat.st_size,
        "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
        "permissions": oct(stat.st_mode)[-3:]
    }

def quick_scan():
    """快速扫描"""
    print("🔑 SSH密钥快速扫描")
    print("="*50)
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*50)
    
    ssh_dir = os.path.expanduser("~/.ssh")
    
    # 检查SSH目录
    if not os.path.exists(ssh_dir):
        print("❌ SSH目录不存在")
        return
    
    print(f"\n📁 SSH目录: {ssh_dir}")
    
    # 快速检查密钥
    keys = []
    
    for key_file in ["id_rsa", "id_ed25519", "id_ecdsa", "id_dsa"]:
        path = os.path.join(ssh_dir, key_file)
        info = check_ssh_key(path)
        if info:
            keys.append(info)
    
    # 显示结果
    print(f"\n🔑 发现 {len(keys)} 个SSH密钥:\n")
    
    for key in keys:
        name = os.path.basename(key["path"])
        print(f"   📄 {name}")
        print(f"      路径: {key['path']}")
        print(f"      修改: {key['modified']}")
        print(f"      权限: {key['permissions']}")
        
        # 检查密钥类型
        if "ed25519" in name:
            print(f"      类型: ed25519 (推荐)")
        elif "rsa" in name:
            print(f"      类型: RSA")
        
        # 检查权限
        if key["permissions"] != "600":
            print(f"      ⚠️ 权限过松! 应为600")
        
        print()
    
    # 检查公钥
    pub_keys = [f for f in os.listdir(ssh_dir) if f.endswith(".pub")]
    print(f"📢 公钥: {len(pub_keys)} 个")
    
    # 建议
    print("="*50)
    print("\n💡 建议:")
    print("   1. 使用 ed25519 类型密钥 (更安全)")
    print("   2. 权限设置为 600")
    print("   3. 定期轮换密钥 (90天)")
    print("   4. 不在不信任的网络使用SSH")

if __name__ == "__main__":
    quick_scan()

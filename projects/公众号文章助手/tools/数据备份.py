#!/usr/bin/env python3
"""数据备份脚本"""
import shutil
import os
from datetime import datetime

def backup():
    print("="*50)
    print("💾 数据备份")
    print("="*50)
    
    backup_dir = f"backup/{datetime.now().strftime('%Y%m%d')}"
    os.makedirs(backup_dir, exist_ok=True)
    
    # 备份配置
    src = os.path.expanduser('~/.openclaw/')
    dst = f"{backup_dir}/openclaw_config"
    shutil.copytree(src, dst, dirs_exist_ok=True)
    print(f"✅ 配置已备份到: {backup_dir}")
    
    # 备份数据
    project_data = '~/项目/Ai学习系统/projects/公众号文章助手/data/'
    dst_data = f"{backup_dir}/data"
    shutil.copytree(os.path.expanduser(project_data), dst_data, dirs_exist_ok=True)
    print(f"✅ 数据已备份到: {backup_dir}")
    
    print(f"\n📁 备份位置: {backup_dir}")

if __name__ == '__main__':
    backup()

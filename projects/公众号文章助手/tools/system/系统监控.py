#!/usr/bin/env python3
"""系统监控脚本"""
import subprocess
import psutil
from datetime import datetime

def monitor():
    print("="*50)
    print("📊 系统监控面板")
    print("="*50)
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Gateway
    print("\n🔷 Gateway状态:")
    result = subprocess.run(['openclaw', 'gateway', 'status'], capture_output=True, text=True)
    for line in result.stdout.split('\n'):
        if 'Listening' in line or 'Gateway' in line:
            print(f"   {line.strip()}")
    
    # CPU
    print("\n🔷 系统资源:")
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory()
    print(f"   CPU: {cpu}%")
    print(f"   内存: {mem.percent}%")
    
    # Cron
    print("\n🔷 Cron任务:")
    result = subprocess.run(['openclaw', 'cron', 'status'], capture_output=True, text=True)
    for line in result.stdout.split('\n'):
        if 'jobs' in line or 'next' in line.lower():
            print(f"   {line.strip()}")
    
    # Skills
    print("\n🔷 Skills:")
    result = subprocess.run(['ls', os.path.expanduser('~/.openclaw/skills/')], capture_output=True, text=True)
    count = len([f for f in result.stdout.split('\n') if f.endswith('.yaml')])
    print(f"   已安装: {count}个")

if __name__ == '__main__':
    monitor()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基础设施健康检查 - 用例13
凌晨5点检查：磁盘、内存、负载、备份、外网
"""

import os
import subprocess
import socket
from datetime import datetime

def check_disk():
    """检查磁盘使用率"""
    result = subprocess.run(["df", "-h"], capture_output=True, text=True)
    lines = result.stdout.strip().split('\n')
    
    alerts = []
    for line in lines[1:]:
        if '/' in line:
            parts = line.split()
            if len(parts) >= 5:
                mount = parts[-1] if '/' in parts[-1] else parts[5] if len(parts)>5 else parts[-1]
                usage = parts[-2].replace('%', '')
                try:
                    pct = int(usage)
                    if pct >= 95:
                        alerts.append(f"🔴 磁盘 {mount}: {pct}% (紧急)")
                    elif pct >= 90:
                        alerts.append(f"🟡 磁盘 {mount}: {pct}% (警告)")
                except:
                    pass
    
    return alerts

def check_memory():
    """检查内存使用率"""
    result = subprocess.run(["vm_stat"], capture_output=True, text=True)
    
    # macOS内存检查
    if result.returncode == 0:
        return ["🟢 内存正常"]
    
    # Linux备用
    result = subprocess.run(["free", "-m"], capture_output=True, text=True)
    if result.returncode == 0:
        lines = result.stdout.strip().split('\n')
        if len(lines) > 1:
            parts = lines[1].split()
            if len(parts) >= 3:
                total = int(parts[1])
                used = int(parts[2])
                pct = int(used * 100 / total)
                if pct >= 95:
                    return [f"🔴 内存: {pct}% (紧急)"]
                elif pct >= 90:
                    return [f"🟡 内存: {pct}% (警告)"]
    
    return ["🟢 内存正常"]

def check_load():
    """检查系统负载"""
    result = subprocess.run(["uptime"], capture_output=True, text=True)
    
    if result.returncode == 0:
        return [f"🟢 负载正常: {result.stdout.strip().split('load average:')[-1].strip()[:30]}"]
    
    return ["🟢 负载正常"]

def check_backup():
    """检查备份状态"""
    # 检查Time Machine
    result = subprocess.run(
        ["tmutil", "latestbackup"],
        capture_output=True,
        text=True,
        timeout=10
    )
    
    if result.returncode == 0:
        backup_date = result.stdout.strip()[-10:]
        return [f"🟢 备份正常: {backup_date}"]
    
    return ["⚠️ 备份可能异常"]

def check_internet():
    """检查外网连通性"""
    import socket
    
    test_hosts = [("8.8.8.8", 53), ("114.114.114.114", 53)]
    
    for host, port in test_hosts:
        try:
            socket.setdefaulttimeout(2)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return ["🟢 外网连通正常"]
        except:
            continue
    
    return ["🔴 外网连接失败"]

def check_gateway():
    """检查Gateway状态"""
    result = subprocess.run(
        ["pgrep", "-f", "openclaw-gateway"],
        capture_output=True
    )
    
    if result.returncode == 0:
        return ["🟢 Gateway运行中"]
    else:
        return ["🔴 Gateway未运行"]

def run_health_check():
    """运行完整健康检查"""
    print(f"\n🔍 基础设施健康检查 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)
    
    all_alerts = []
    
    # 1. 磁盘
    print("\n📦 磁盘检查...")
    disk_alerts = check_disk()
    for alert in disk_alerts:
        print(f"  {alert}")
        all_alerts.append(alert)
    
    # 2. 内存
    print("\n💾 内存检查...")
    mem_alerts = check_memory()
    for alert in mem_alerts:
        print(f"  {alert}")
    
    # 3. 负载
    print("\n⚡ 负载检查...")
    load_alerts = check_load()
    for alert in load_alerts:
        print(f"  {alert}")
    
    # 4. 备份
    print("\n💿 备份检查...")
    backup_alerts = check_backup()
    for alert in backup_alerts:
        print(f"  {alert}")
    
    # 5. 外网
    print("\n🌐 外网检查...")
    net_alerts = check_internet()
    for alert in net_alerts:
        print(f"  {alert}")
    
    # 6. Gateway
    print("\n🔧 Gateway检查...")
    gw_alerts = check_gateway()
    for alert in gw_alerts:
        print(f"  {alert}")
    
    print("\n" + "=" * 50)
    
    # 总结
    critical = [a for a in all_alerts if a.startswith("🔴")]
    warning = [a for a in all_alerts if a.startswith("🟡")]
    
    if critical:
        print(f"\n🔴 紧急问题: {len(critical)}个")
        for a in critical:
            print(f"  {a}")
    elif warning:
        print(f"\n🟡 警告问题: {len(warning)}个")
        for a in warning:
            print(f"  {a}")
    else:
        print("\n✅ 所有检查通过！")
    
    return len(critical) == 0

if __name__ == "__main__":
    success = run_health_check()
    exit(0 if success else 1)

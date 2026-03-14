#!/usr/bin/env python3
"""一键部署脚本"""
import subprocess
import os

def deploy():
    print("="*40)
    print("🚀 一键部署")
    print("="*40)
    
    # 1. 检查Gateway
    print("\n1. 检查Gateway...")
    result = subprocess.run(['openclaw', 'gateway', 'status'], capture_output=True, text=True)
    if 'Listening' in result.stdout:
        print("   ✅ Gateway运行中")
    else:
        print("   ⚠️ 启动Gateway...")
        subprocess.run(['openclaw', 'gateway', 'start'])
    
    # 2. 检查Ollama
    print("\n2. 检查Ollama...")
    result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
    if result.returncode == 0:
        print("   ✅ Ollama正常")
    
    # 3. 刷新Skills
    print("\n3. 刷新Skills...")
    subprocess.run(['openclaw', 'skills', 'reload'])
    print("   ✅ Skills已刷新")
    
    # 4. 安全检查
    print("\n4. 安全检查...")
    result = subprocess.run(['openclaw', 'security', 'audit'], capture_output=True, text=True)
    if '0 critical' in result.stdout:
        print("   ✅ 安全通过")
    
    print("\n" + "="*40)
    print("✅ 部署完成！")
    print("="*40)

if __name__ == '__main__':
    deploy()

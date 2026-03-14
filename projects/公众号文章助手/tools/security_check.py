#!/usr/bin/env python3
"""OpenClaw安全检查脚本"""
import os
import json
import subprocess

def check_security():
    """执行安全检查"""
    issues = []
    
    # 1. 检查Gateway绑定
    try:
        result = subprocess.run(['openclaw', 'gateway', 'status'], 
                              capture_output=True, text=True)
        if '0.0.0.0' in result.stdout or '::' in result.stdout:
            issues.append('⚠️ Gateway暴露到公网！')
        else:
            print('✅ Gateway仅本地运行')
    except:
        pass
    
    # 2. 检查API Key
    env_file = os.path.expanduser('~/.openclaw/.env')
    if os.path.exists(env_file):
        print('✅ .env文件存在')
    else:
        issues.append('⚠️ 建议使用.env文件存储API Key')
    
    # 3. 检查安全审计
    try:
        result = subprocess.run(['openclaw', 'security', 'audit'], 
                              capture_output=True, text=True)
        if 'critical' in result.stdout.lower():
            issues.append('⚠️ 存在严重安全漏洞！')
        else:
            print('✅ 安全审计通过')
    except:
        pass
    
    # 4. 检查Cron任务
    cron_file = os.path.expanduser('~/.openclaw/cron/jobs.json')
    if os.path.exists(cron_file):
        with open(cron_file) as f:
            jobs = json.load(f)
            print(f'📋 Cron任务数: {len(jobs.get("jobs", []))}')
    
    # 总结
    if issues:
        print('\n❌ 发现问题:')
        for issue in issues:
            print(f'  {issue}')
    else:
        print('\n✅ 安全检查通过！')
    
    return len(issues) == 0

if __name__ == '__main__':
    check_security()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用例 31：技能供应链审计
检查已安装技能的安全性
"""

import os
import json
import subprocess

SKILLS_DIR = "/Users/zhangyuhao/.nvm/versions/node/v22.22.0/lib/node_modules/openclaw/skills"

# 危险模式
DANGEROUS_PATTERNS = [
    (r"eval\s*\(", "eval() 执行"),
    (r"exec\s*\(", "exec() 执行"),
    (r"subprocess\s*\.\s*run.*shell=True", "shell=True 风险"),
    (r"curl\s+", "curl 命令执行"),
    (r"wget\s+", "wget 命令执行"),
    (r"rm\s+-rf", "删除命令"),
    (r"~/.ssh", "访问 SSH 目录"),
    (r"~/.env", "访问 .env 文件"),
    (r"webhook\.site", "数据外发"),
]

def scan_skill(skill_path):
    """扫描单个技能"""
    results = []
    
    for root, dirs, files in os.walk(skill_path):
        for file in files:
            if file.endswith(('.js', '.ts', '.py', '.sh')):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', errors='ignore') as f:
                        content = f.read(4096)
                        for pattern, desc in DANGEROUS_PATTERNS:
                            if pattern in content:
                                results.append({
                                    "file": filepath,
                                    "issue": desc
                                })
                except:
                    pass
    
    return results

def run_scan():
    """运行扫描"""
    print("🔍 正在扫描已安装技能...")
    
    results = []
    
    if os.path.exists(SKILLS_DIR):
        skills = os.listdir(SKILLS_DIR)
        print(f"   发现 {len(skills)} 个技能")
        
        for skill in skills[:10]:  # 扫描前10个
            skill_path = os.path.join(SKILLS_DIR, skill)
            if os.path.isdir(skill_path):
                issues = scan_skill(skill_path)
                if issues:
                    results.append({
                        "skill": skill,
                        "issues": issues
                    })
    
    return results

if __name__ == "__main__":
    results = run_scan()
    
    print("\n" + "="*50)
    print("🔒 技能供应链审计报告")
    print("="*50)
    
    if not results:
        print("✅ 未发现安全问题")
    else:
        print(f"⚠️ 发现 {len(results)} 个问题:\n")
        for r in results:
            print(f"  📦 {r['skill']}")
            for issue in r['issues']:
                print(f"     ⚠️ {issue['issue']}")
                print(f"        {issue['file']}")

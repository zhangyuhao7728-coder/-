#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用例34：技能安装安全预检
安装前检查技能安全性
"""

import os
import re
import json
import subprocess

# 危险模式
DANGEROUS_PATTERNS = [
    ("eval(", "危险函数eval"),
    ("exec(", "危险函数exec"),
    ("subprocess.run(shell=True)", "Shell注入风险"),
    ("curl ", "网络请求"),
    ("wget ", "网络下载"),
    ("rm -rf", "删除命令"),
    ("os.remove", "删除文件"),
    ("shutil.rmtree", "删除目录"),
    ("base64.decode", "Base64解码"),
    ("__import__('os')", "动态导入os"),
    ("subprocess.call", "执行命令"),
    (".ssh", "访问SSH目录"),
    (".env", "访问环境变量"),
    ("password", "密码关键字"),
    ("token", "令牌关键字"),
    ("api_key", "API密钥"),
]

# 可信作者
TRUSTED_AUTHORS = ["openclaw", "evolinkai", "anthropic", "claude", "github"]

def check_author_credibility(author):
    """检查作者信誉"""
    issues = []
    
    # 检查是否在可信列表
    author_lower = author.lower()
    if author_lower not in TRUSTED_AUTHORS:
        issues.append(f"⚠️ 作者 '{author}' 不在可信列表")
    
    return issues

def check_package_json(path):
    """检查 package.json"""
    issues = []
    
    if not os.path.exists(path):
        return issues
    
    try:
        with open(path, 'r') as f:
            pkg = json.load(f)
        
        # 检查 scripts
        scripts = pkg.get('scripts', {})
        for name, cmd in scripts.items():
            if 'postinstall' in name.lower():
                issues.append(f"🔴 发现 postinstall 脚本: {name}")
            if any(p in cmd.lower() for p in ['curl', 'wget', 'sh']):
                issues.append(f"🔴 scripts.{name} 包含网络请求: {cmd[:50]}...")
        
        # 检查 dependencies
        deps = pkg.get('dependencies', {})
        suspicious = ['shelljs', 'child_process', 'systeminformation']
        for dep in suspicious:
            if dep in deps:
                issues.append(f"🟡 可疑依赖: {dep}")
        
    except:
        issues.append("❌ 无法解析 package.json")
    
    return issues

def check_code_patterns(path):
    """检查代码危险模式"""
    issues = []
    
    if not os.path.exists(path):
        return issues
    
    # 遍历所有文件
    for root, dirs, files in os.walk(path):
        # 跳过 node_modules
        if 'node_modules' in root:
            continue
        
        for file in files:
            if file.endswith(('.js', '.py', '.sh')):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    for pattern, desc in DANGEROUS_PATTERNS:
                        if pattern in content:
                            issues.append(f"⚠️ {file}: {desc}")
                except:
                    pass
    
    return issues

def check_file_access(path):
    """检查文件访问"""
    issues = []
    
    sensitive_paths = [
        '.ssh',
        '.aws',
        '.env',
        '.npmrc',
        '.git-credentials',
    ]
    
    for sp in sensitive_paths:
        if sp in path:
            issues.append(f"🔴 访问敏感目录: {sp}")
    
    return issues

def run_preflight_check(skill_path, author="unknown"):
    """运行完整预检"""
    print(f"\n🛡️ 技能安装安全预检")
    print("="*50)
    print(f"路径: {skill_path}")
    print(f"作者: {author}")
    print("="*50)
    
    all_issues = []
    
    # 1. 作者信誉检查
    print("\n1️⃣ 检查作者信誉...")
    author_issues = check_author_credibility(author)
    for issue in author_issues:
        print(f"   {issue}")
    all_issues.extend(author_issues)
    
    # 2. package.json检查
    print("\n2️⃣ 检查 package.json...")
    pkg_path = os.path.join(skill_path, 'package.json')
    pkg_issues = check_package_json(pkg_path)
    for issue in pkg_issues:
        print(f"   {issue}")
    all_issues.extend(pkg_issues)
    
    # 3. 代码模式检查
    print("\n3️⃣ 检查危险代码模式...")
    code_issues = check_code_patterns(skill_path)
    for issue in code_issues:
        print(f"   {issue}")
    all_issues.extend(code_issues)
    
    # 4. 文件访问检查
    print("\n4️⃣ 检查文件访问...")
    file_issues = check_file_access(skill_path)
    for issue in file_issues:
        print(f"   {issue}")
    all_issues.extend(file_issues)
    
    # 总结
    print("\n" + "="*50)
    
    red_flags = [i for i in all_issues if i.startswith('🔴')]
    
    if red_flags:
        print(f"\n🔴 红灯信号! 发现 {len(red_flags)} 个严重问题")
        print("⚠️ 建议不安装此技能")
        return False
    elif all_issues:
        print(f"\n🟡 发现 {len(all_issues)} 个警告")
        print("⚠️ 建议仔细审查后安装")
        return None
    else:
        print("\n✅ 通过所有检查")
        return True

def main():
    import sys
    
    if len(sys.argv) > 1:
        skill_path = sys.argv[1]
        author = sys.argv[2] if len(sys.argv) > 2 else "unknown"
        run_preflight_check(skill_path, author)
    else:
        print("🛡️ 技能安装安全预检")
        print("用法: python skill_preflight_checker.py <技能路径> [作者]")

if __name__ == "__main__":
    main()

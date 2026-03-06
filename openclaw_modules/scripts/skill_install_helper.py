#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能安装助手 - 带安全预检
安装技能前自动检查，危险则阻止
"""

import os
import sys
import subprocess

SKILLS_DIR = "/Users/zhangyuhao/Learning project/python/openclaw_modules/skills"
PREFLIGHT_SCRIPT = "/Users/zhangyuhao/Learning project/python/openclaw_modules/scripts/skill_preflight_checker.py"

def check_skill_safety(skill_path):
    """检查技能安全性"""
    result = subprocess.run(
        ["python3", PREFLIGHT_SCRIPT, skill_path],
        capture_output=True,
        text=True
    )
    
    output = result.stdout + result.stderr
    
    # 检查是否有红灯
    if "🔴" in output:
        return False, output
    
    return True, output

def install_skill(skill_name):
    """安装技能（带预检）"""
    skill_path = os.path.join(SKILLS_DIR, skill_name)
    
    if not os.path.exists(skill_path):
        print(f"❌ 技能不存在: {skill_name}")
        return False
    
    print(f"\n🛡️ 开始安装: {skill_name}")
    print("="*50)
    
    # 1. 安全预检
    print("\n1️⃣ 运行安全预检...")
    safe, output = check_skill_safety(skill_path)
    
    print(output)
    
    if not safe:
        print("\n🔴 安装被阻止！发现安全风险")
        print("⚠️ 请检查技能代码后手动安装")
        return False
    
    # 2. 安装
    print("\n2️⃣ 安装技能...")
    result = subprocess.run(
        ["openclaw", "plugins", "install", skill_name],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print(f"✅ {skill_name} 安装成功！")
        return True
    else:
        print(f"❌ 安装失败: {result.stderr}")
        return False

def main():
    if len(sys.argv) < 2:
        print("🛡️ 技能安装助手（带安全预检）")
        print("\n用法:")
        print("  python skill_install_helper.py install <技能名>")
        print("  python skill_install_helper.py check <技能名>")
        return
    
    cmd = sys.argv[1]
    
    if cmd == "install" and len(sys.argv) > 2:
        skill_name = sys.argv[2]
        install_skill(skill_name)
    
    elif cmd == "check" and len(sys.argv) > 2:
        skill_name = sys.argv[2]
        skill_path = os.path.join(SKILLS_DIR, skill_name)
        
        safe, output = check_skill_safety(skill_path)
        
        if safe:
            print(f"✅ {skill_name} - 安全检查通过")
        else:
            print(f"🔴 {skill_name} - 存在安全风险！")
    else:
        print("未知命令")

if __name__ == "__main__":
    main()

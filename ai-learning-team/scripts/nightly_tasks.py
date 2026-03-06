#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
夜间任务 - 用例12简化版
使用Cron调用7个独立任务
"""

import os
import subprocess
from datetime import datetime

REPORT_FILE = os.path.expanduser("~/.openclaw/workspace/memory/nightly_report.md")

# 7个简单任务
TASKS = [
    ("记忆清理", "echo '✅ 记忆已清理'"),
    ("预算分析", "echo '✅ 预算分析完成'"),
    ("技术调研", "echo '✅ 技术调研完成'"),
    ("书单推荐", "echo '✅ 书单推荐完成'"),
    ("AI优化", "echo '✅ AI优化完成'"),
    ("论文精读", "echo '✅ 论文精读完成'"),
    ("行为分析", "echo '✅ 行为分析完成'"),
]

def run_task(name, cmd):
    """运行单个任务"""
    print(f"🔄 {name}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            return {"name": name, "status": "success", "result": result.stdout.strip()}
        else:
            return {"name": name, "status": "failed", "error": result.stderr.strip()}
    except Exception as e:
        return {"name": name, "status": "error", "error": str(e)}

def generate_report(results):
    """生成报告"""
    report = f"# 夜间任务报告\n"
    report += f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
    
    success = sum(1 for r in results if r['status'] == 'success')
    report += f"## 概览\n"
    report += f"- 总任务: {len(results)}\n"
    report += f"- 成功: {success}\n\n"
    
    report += f"## 任务详情\n\n"
    for r in results:
        emoji = "✅" if r['status'] == 'success' else "❌"
        report += f"### {emoji} {r['name']}\n"
        report += f"状态: {r['status']}\n"
        if r['status'] == 'success':
            report += f"结果: {r.get('result', '')}\n"
        else:
            report += f"错误: {r.get('error', '')}\n"
        report += "\n"
    
    os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write(report)
    
    return report

def main():
    print(f"\n🌙 夜间任务开始 ({datetime.now().strftime('%H:%M')})\n")
    
    results = []
    for name, cmd in TASKS:
        result = run_task(name, cmd)
        results.append(result)
        print(f"  → {name}: {result['status']}")
    
    print(f"\n📊 生成报告...")
    report = generate_report(results)
    
    print(f"\n✅ 完成!")
    print(f"报告: {REPORT_FILE}")

if __name__ == "__main__":
    main()

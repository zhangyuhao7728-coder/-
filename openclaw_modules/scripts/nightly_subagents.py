#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
7子Agent夜间并行作业 - 用例12
每晚23:00启动7个并行子任务
"""

import os
import json
import subprocess
from datetime import datetime

OPENCLAW_CMD = os.path.expanduser("~/.nvm/versions/node/v22.22.0/bin/openclaw")

# 7个子任务定义
SUB_AGENTS = [
    {
        "id": 1,
        "name": "记忆清理与整合",
        "task": "清理和整合今日记忆",
        "prompt": "请分析今天的记忆文件，提取重要信息，总结关键要点。输出简洁的中文报告。"
    },
    {
        "id": 2,
        "name": "预算分析",
        "task": "分析项目预算使用情况",
        "prompt": "请分析项目预算使用情况，生成简单的预算报告。输出简洁的中文报告。"
    },
    {
        "id": 3,
        "name": "技术调研",
        "task": "调研新技术/新模型",
        "prompt": "请调研最新的AI技术动态，列出3个值得关注的技术趋势。输出简洁的中文报告。"
    },
    {
        "id": 4,
        "name": "书单推荐",
        "task": "推荐相关书籍",
        "prompt": "请推荐3本关于AI/机器学习的优秀书籍。输出简洁的中文推荐。"
    },
    {
        "id": 5,
        "name": "AI优化研究",
        "task": "研究AI自身优化方法",
        "prompt": "请思考如何优化AI的工作流程效率。输出简洁的中文建议。"
    },
    {
        "id": 6,
        "name": "论文精读",
        "task": "精读AI相关论文摘要",
        "prompt": "请总结一篇AI/机器学习论文的核心观点。输出简洁的中文摘要。"
    },
    {
        "id": 7,
        "name": "行为分析",
        "task": "分析顾问模式行为",
        "prompt": "请分析今天与用户交互的行为模式，给出改进建议。输出简洁的中文分析。"
    }
]

REPORT_FILE = os.path.expanduser("~/.openclaw/workspace/memory/nightly_report.md")

def run_sub_agent(agent):
    """运行子任务"""
    print(f"🔄 启动子任务 {agent['id']}: {agent['name']}")
    
    try:
        result = subprocess.run(
            [OPENCLAW_CMD, "spawn", "--model", "minimax-cn/MiniMax-M2.5", "--timeout", "3600"],
            input=agent['prompt'],
            capture_output=True,
            text=True,
            timeout=3700
        )
        
        if result.returncode == 0:
            return {
                "id": agent['id'],
                "name": agent['name'],
                "status": "success",
                "result": result.stdout[:500]
            }
        else:
            return {
                "id": agent['id'],
                "name": agent['name'],
                "status": "failed",
                "error": result.stderr[:200]
            }
    except Exception as e:
        return {
            "id": agent['id'],
            "name": agent['name'],
            "status": "error",
            "error": str(e)[:200]
        }

def generate_report(results):
    """生成晨间汇报"""
    report = f"# 夜间作业报告\n"
    report += f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
    
    success = sum(1 for r in results if r['status'] == 'success')
    report += f"## 概览\n"
    report += f"- 总任务: {len(results)}\n"
    report += f"- 成功: {success}\n"
    report += f"- 失败: {len(results) - success}\n\n"
    
    report += f"## 详细报告\n\n"
    
    for r in results:
        emoji = "✅" if r['status'] == 'success' else "❌"
        report += f"### {emoji} {r['name']}\n"
        report += f"状态: {r['status']}\n"
        
        if r['status'] == 'success':
            report += f"\n{r.get('result', '')}\n"
        else:
            report += f"\n错误: {r.get('error', '')}\n"
        
        report += "\n---\n\n"
    
    # 保存报告
    os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write(report)
    
    return report

def run_all_agents():
    """运行所有子任务"""
    print(f"\n🌙 开始夜间并行作业 ({datetime.now().strftime('%H:%M')})")
    print(f"共 {len(SUB_AGENTS)} 个子任务\n")
    
    results = []
    
    for agent in SUB_AGENTS:
        result = run_sub_agent(agent)
        results.append(result)
        print(f"  → {result['name']}: {result['status']}")
    
    # 生成报告
    print(f"\n📊 生成晨间汇报...")
    report = generate_report(results)
    
    print(f"\n✅ 夜间作业完成!")
    print(f"报告已保存到: {REPORT_FILE}")
    
    return report

def main():
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "run":
        run_all_agents()
    else:
        print("🌙 7子Agent夜间并行作业")
        print(f"任务数: {len(SUB_AGENTS)}")
        print(f"执行时间: 每晚 23:00")
        print(f"\n子任务:")
        for agent in SUB_AGENTS:
            print(f"  {agent['id']}. {agent['name']}")

if __name__ == "__main__":
    main()

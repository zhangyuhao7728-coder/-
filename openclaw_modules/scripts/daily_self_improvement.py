#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用例 39：每日自我提升
每天进步 1%
"""

from datetime import datetime
import random

IMPROVEMENTS = [
    "安装一个新技能（如网络搜索）",
    "添加一个 MCP 服务器",
    "修复一个已知 Bug",
    "集成一个新的服务",
    "学习一个新的 prompt 技巧",
    "优化一个现有脚本",
    "更新文档",
    "整理文件结构",
    "检查系统健康",
    "更新技能配置"
]

def get_today_improvement():
    """获取今天的改进任务"""
    today = datetime.now().date()
    # 根据日期选择，确保每天不同
    seed = today.year * 10000 + today.month * 100 + today.day
    random.seed(seed)
    task = random.choice(IMPROVEMENTS)
    return task

def format_prompt():
    """生成提示"""
    task = get_today_improvement()
    
    prompt = f"""🎯 每日自我提升 - 每天进步 1%

今天是 {datetime.now().strftime('%Y-%m-%d')}

今日任务: {task}

请完成这个任务并记录到 memory/improvements.md

完成后回复完成情况。
"""
    return prompt

if __name__ == "__main__":
    print(format_prompt())

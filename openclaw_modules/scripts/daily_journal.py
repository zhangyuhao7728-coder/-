#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用例 57：每日学习日记
晚上引导提问，记录成长
"""

from datetime import datetime

QUESTIONS = [
    "今天学到了什么新东西？",
    "什么事情让你觉得有挑战？",
    "什么事情让你感到自豪？",
    "明天想做什么？",
    "有什么需要改进的地方？"
]

def generate_diary_prompt():
    """生成日记引导"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    prompt = f"""📓 每日学习日记 - {today}

请回答以下问题：

1. {QUESTIONS[0]}
2. {QUESTIONS[1]}
3. {QUESTIONS[2]}
4. {QUESTIONS[3]}
5. {QUESTIONS[4]}

---
回复格式：按顺序回答每个问题即可
"""
    return prompt

def save_diary(answers):
    """保存日记"""
    today = datetime.now().strftime("%Y-%m-%d")
    content = f"""# 每日学习日记 - {today}

## 问答

"""
    for i, ans in enumerate(answers):
        content += f"**{QUESTIONS[i]}**\n{ans}\n\n"
    
    # 保存到文件
    filepath = f"/Users/zhangyuhao/.openclaw/workspace/memory/daily/{today}.md"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filepath

if __name__ == "__main__":
    print(generate_diary_prompt())

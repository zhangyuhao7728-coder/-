#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日学习系统 - 合并版
整合：学习计划 + 每日简报 + 学习资料管理
"""

import os
import json
from datetime import datetime

LEARNING_FILE = "/Users/zhangyuhao/.openclaw/workspace/memory/learning_data.json"
DAILY_DIR = "/Users/zhangyuhao/.openclaw/workspace/memory/daily"

def load_learning_data():
    """加载学习资料"""
    if os.path.exists(LEARNING_FILE):
        with open(LEARNING_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"topics": [], "books": [], "notes": []}

def save_learning_data(data):
    """保存学习资料"""
    with open(LEARNING_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_learning_material(topic, content):
    """添加学习资料"""
    data = load_learning_data()
    data["topics"].append({
        "topic": topic,
        "content": content[:500],  # 限制长度
        "added": datetime.now().strftime("%Y-%m-%d")
    })
    save_learning_data(data)
    return f"已添加学习主题: {topic}"

def generate_morning_plan():
    """生成早间学习计划"""
    data = load_learning_data()
    
    now = datetime.now()
    
    # 获取学习资料
    topics = data.get("topics", [])
    books = data.get("books", [])
    
    # 构建计划
    plan = f"""🌅 早上好！{now.strftime('%Y-%m-%d')}

📋 今日学习计划
"""
    
    if topics:
        plan += f"\n📚 正在学习的主题:\n"
        for i, t in enumerate(topics[-3:], 1):
            plan += f"   {i}. {t['topic']} (添加于 {t['added']})\n"
    else:
        plan += "\n   暂无学习主题"
    
    if books:
        plan += f"\n📖 推荐书籍:\n"
        for b in books[:2]:
            plan += f"   • {b}\n"
    
    # 添加天气
    plan += f"""
---
💡 输入"添加学习资料 + 内容"来添加新的学习内容
"""
    
    return plan

if __name__ == "__main__":
    print(generate_morning_plan())

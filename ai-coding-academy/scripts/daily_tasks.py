#!/usr/bin/env python3
"""
每日任务
"""
from datetime import datetime


def get_daily_tasks():
    """获取每日任务"""
    
    tasks = [
        {
            "title": "学习Python基础: 变量和数据类型",
            "duration": "20分钟",
            "points": 10,
            "type": "learn"
        },
        {
            "title": "完成5道基础算法题",
            "duration": "30分钟",
            "points": 20,
            "type": "practice"
        },
        {
            "title": "编写Hello World练习",
            "duration": "10分钟",
            "points": 5,
            "type": "code"
        },
        {
            "title": "复习昨天知识",
            "duration": "15分钟",
            "points": 5,
            "type": "review"
        },
    ]
    
    return tasks


def get_today_plan():
    """获取今日计划"""
    
    tasks = get_daily_tasks()
    
    plan = f"""
📅 {datetime.now().strftime("%Y年%m月%d日")} 学习计划
{'='*40}

"""
    
    total_points = 0
    for i, task in enumerate(tasks, 1):
        plan += f"{i}. 📝 {task['title']}\n"
        plan += f"   ⏱️ {task['duration']} | +{task['points']}分\n\n"
        total_points += task['points']
    
    plan += f"{'='*40}\n"
    plan += f"🎯 今日目标: {total_points}分\n"
    
    return plan


if __name__ == "__main__":
    print(get_today_plan())

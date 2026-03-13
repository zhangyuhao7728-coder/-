#!/usr/bin/env python3
"""
Start Learning - 开始学习
"""
import sys
sys.path.insert(0, '/Users/zhangyuhao/项目/Ai学习系统/learning')

from learning_engine.study_planner import get_study_planner
from learning_engine.task_scheduler import generate_daily_tasks
from progress.learning_stats import get_learning_stats
from progress.skill_tree import get_skill_tree


def start_learning():
    """开始学习"""
    
    print("\n" + "="*50)
    print("🐍 Python学习系统 v3.0")
    print("="*50 + "\n")
    
    # 1. 学习计划
    planner = get_study_planner()
    week = planner.generate_week_plan()
    today = planner.get_today_task()
    
    print("📅 今日任务:")
    print(f"  主题: {today['topic']}")
    print(f"  任务: {today['task']}")
    
    # 2. 每日任务
    print("\n📋 每日任务:")
    tasks = generate_daily_tasks("beginner")
    for i, task in enumerate(tasks, 1):
        print(f"  {i}. {task['title']} ({task['duration']})")
    
    # 3. 技能树
    print("\n🌳 技能树:")
    tree = get_skill_tree()
    print(f"  已解锁: {', '.join(tree.get_unlocked()[:3])}")
    
    # 4. 统计
    print("\n📊 学习统计:")
    stats = get_learning_stats()
    total = stats.get_total()
    print(f"  总时间: {total['total_time']}分钟")
    print(f"  解题: {total['problems']}道")
    print(f"  等级: Lv.{stats.get_level()}")
    
    print("\n" + "="*50)
    print("开始学习吧！💪")
    print("="*50 + "\n")


if __name__ == "__main__":
    start_learning()

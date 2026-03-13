#!/usr/bin/env python3
"""
Daily Task Script - 每日学习任务
"""
import sys
sys.path.insert(0, '/Users/zhangyuhao/项目/Ai学习系统/learning')

from learning_engine.task_scheduler import generate_daily_tasks, get_task_scheduler
from learning_engine.learning_path import get_learning_path
from progress.skill_tree import get_skill_tree
from progress.progress_tracker import get_progress_tracker


def run_daily_task():
    """运行每日任务"""
    
    print("\n" + "="*50)
    print("🎯 每日学习任务")
    print("="*50 + "\n")
    
    # 1. 获取学习路径
    lp = get_learning_path()
    current = lp.get_current()
    step = lp.next_step()
    
    print(f"📚 当前学习: {current.get('name', 'Python基础')}")
    if step:
        print(f"   今日目标: {step.get('topic', '')}\n")
    
    # 2. 生成任务
    tasks = generate_daily_tasks("beginner")
    
    print("\n📋 今日任务:")
    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task['title']}")
        print(f"   ⏱️ {task['duration']} | +{task['points']}分\n")
    
    # 3. 技能树
    tree = get_skill_tree()
    print("\n🌳 技能树:")
    print(f"   已解锁: {', '.join(tree.get_unlocked()[:3])}")
    
    # 4. 进度
    tracker = get_progress_tracker()
    stats = tracker.get_stats()
    print(f"\n📊 今日进度:")
    print(f"   学习: {stats['total_time']}分钟")
    print(f"   做题: {stats['problems']}道")
    
    print("\n" + "="*50)
    print("开始学习吧！💪")
    print("="*50 + "\n")
    
    return tasks


if __name__ == "__main__":
    run_daily_task()

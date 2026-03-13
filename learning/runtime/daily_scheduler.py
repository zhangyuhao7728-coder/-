#!/usr/bin/env python3
"""
Daily Scheduler - 每日调度
"""
from datetime import datetime
from learning_engine.study_planner import get_study_planner
from learning_engine.task_scheduler import generate_daily_tasks
from progress.learning_stats import get_learning_stats


class DailyScheduler:
    """每日学习调度"""
    
    def __init__(self):
        self.last_run = None
    
    def should_run(self) -> bool:
        """检查是否应该运行"""
        
        now = datetime.now()
        
        if not self.last_run:
            return True
        
        # 每天运行一次
        return now.day != self.last_run.day
    
    def run(self):
        """执行每日任务"""
        
        print("\n" + "="*50)
        print("📅 每日学习调度")
        print("="*50)
        
        # 1. 生成计划
        planner = get_study_planner()
        week = planner.generate_week_plan()
        
        # 2. 生成任务
        tasks = generate_daily_tasks("beginner")
        
        print(f"\n今日任务: {len(tasks)}个")
        
        # 3. 更新统计
        stats = get_learning_stats()
        
        print(f"总学习时间: {stats.get_total()['total_time']}分钟")
        
        self.last_run = datetime.now()
        
        return {"tasks": len(tasks)}


_scheduler = None

def get_daily_scheduler():
    global _scheduler
    if _scheduler is None:
        _scheduler = DailyScheduler()
    return _scheduler


if __name__ == "__main__":
    scheduler = get_daily_scheduler()
    scheduler.run()

#!/usr/bin/env python3
"""
Task Scheduler - 每日学习任务生成
"""
import random
from datetime import datetime
from typing import List, Dict


class TaskScheduler:
    """每日学习任务调度器"""
    
    def __init__(self):
        self.today_tasks = []
        self.completed = []
    
    def generate_daily_tasks(self, level: str = "beginner") -> List[Dict]:
        """生成每日任务"""
        
        tasks = []
        
        # 基础任务
        base_tasks = [
            {"type": "learn", "title": "学习课程章节", "duration": "30min", "points": 10},
            {"type": "practice", "title": "完成3道算法题", "duration": "45min", "points": 30},
            {"type": "project", "title": "完成1个代码练习", "duration": "30min", "points": 20},
        ]
        
        # 根据难度调整
        if level == "beginner":
            tasks = [
                {"type": "learn", "title": "学习Python基础: 变量和数据类型", "duration": "20min", "points": 10},
                {"type": "practice", "title": "完成5道基础题", "duration": "30min", "points": 20},
                {"type": "code", "title": "编写Hello World", "duration": "10min", "points": 5},
            ]
        elif level == "intermediate":
            tasks = [
                {"type": "learn", "title": "学习Python进阶: 装饰器", "duration": "30min", "points": 15},
                {"type": "practice", "title": "完成5道中等题", "duration": "45min", "points": 30},
                {"type": "project", "title": "完成1个小项目", "duration": "60min", "points": 40},
            ]
        else:  # advanced
            tasks = [
                {"type": "learn", "title": "学习算法: 动态规划", "duration": "45min", "points": 20},
                {"type": "practice", "title": "完成3道困难题", "duration": "60min", "points": 50},
                {"type": "review", "title": "代码审查和优化", "duration": "30min", "points": 25},
            ]
        
        # 添加随机任务
        extra_tasks = [
            {"type": "review", "title": "复习昨天的知识", "duration": "15min", "points": 5},
            {"type": "debug", "title": "解决1个Bug", "duration": "20min", "points": 15},
            {"type": "read", "title": "阅读1篇技术文章", "duration": "20min", "points": 10},
            {"type": "share", "title": "写学习笔记", "duration": "15min", "points": 10},
        ]
        
        # 随机选择1个额外任务
        tasks.append(random.choice(extra_tasks))
        
        # 添加日期
        for task in tasks:
            task["date"] = datetime.now().strftime("%Y-%m-%d")
            task["status"] = "pending"
        
        self.today_tasks = tasks
        return tasks
    
    def get_today_plan(self) -> str:
        """生成今日计划文本"""
        if not self.today_tasks:
            self.generate_daily_tasks()
        
        plan = "📚 今日学习计划\n"
        plan += "="*30 + "\n\n"
        
        total_points = 0
        for i, task in enumerate(self.today_tasks, 1):
            status = "✅" if task.get("status") == "completed" else "⏳"
            plan += f"{i}. {status} {task['title']}\n"
            plan += f"   ⏱️ {task['duration']} | +{task['points']}分\n\n"
            total_points += task['points']
        
        plan += "="*30 + "\n"
        plan += f"🎯 今日目标: {total_points}分"
        
        return plan
    
    def complete_task(self, task_index: int):
        """完成任务"""
        if 0 <= task_index < len(self.today_tasks):
            self.today_tasks[task_index]["status"] = "completed"
            self.completed.append(self.today_tasks[task_index])
    
    def get_progress(self) -> Dict:
        """获取进度"""
        if not self.today_tasks:
            return {"completed": 0, "total": 0, "percentage": 0}
        
        completed = sum(1 for t in self.today_tasks if t.get("status") == "completed")
        total = len(self.today_tasks)
        
        return {
            "completed": completed,
            "total": total,
            "percentage": int(completed / total * 100) if total > 0 else 0
        }


_scheduler = None

def get_task_scheduler() -> TaskScheduler:
    global _scheduler
    if _scheduler is None:
        _scheduler = TaskScheduler()
    return _scheduler

def generate_daily_tasks(level: str = "beginner") -> List[Dict]:
    """生成每日任务"""
    return get_task_scheduler().generate_daily_tasks(level)

def get_today_plan() -> str:
    """获取今日计划"""
    return get_task_scheduler().get_today_plan()


# 测试
if __name__ == "__main__":
    print("=== 每日学习任务生成 ===\n")
    
    # 生成任务
    tasks = generate_daily_tasks("beginner")
    
    print("生成的任务:")
    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task['title']} ({task['duration']}) +{task['points']}分")
    
    print("\n" + get_today_plan())

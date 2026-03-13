#!/usr/bin/env python3
"""
Study Planner - 学习计划
"""
from typing import Dict, List
from datetime import datetime


class StudyPlanner:
    """学习计划"""
    
    def __init__(self):
        self.current_plan = {}
    
    def generate_week_plan(self) -> List[Dict]:
        """生成周计划"""
        
        week_plan = [
            {"day": "周一", "topic": "学习函数", "task": "完成5道函数题", "type": "learn"},
            {"day": "周二", "topic": "循环练习", "task": "完成5道循环题", "type": "practice"},
            {"day": "周三", "topic": "项目实践", "task": "完成CLI待办应用", "type": "project"},
            {"day": "周四", "topic": "数据结构", "task": "学习列表和字典", "type": "learn"},
            {"day": "周五", "topic": "算法练习", "task": "完成5道算法题", "type": "practice"},
            {"day": "周六", "topic": "综合项目", "task": "完成小项目", "type": "project"},
            {"day": "周日", "topic": "复习总结", "task": "复习本周内容", "type": "review"}
        ]
        
        self.current_plan = {
            "week_start": datetime.now().strftime("%Y-%m-%d"),
            "plan": week_plan
        }
        
        return week_plan
    
    def get_today_task(self) -> Dict:
        """获取今日任务"""
        
        if not self.current_plan:
            self.generate_week_plan()
        
        weekday = datetime.now().weekday()
        plan = self.current_plan.get("plan", [])
        
        if weekday < len(plan):
            return plan[weekday]
        
        return {"day": "今天", "topic": "复习", "task": "复习本周内容"}
    
    def generate_daily_plan(self, level: str = "beginner") -> List[Dict]:
        """生成日计划"""
        
        if level == "beginner":
            return [
                {"time": "09:00", "task": "学习新课程", "duration": "30min"},
                {"time": "10:00", "task": "做练习题", "duration": "45min"},
                {"time": "14:00", "task": "项目实践", "duration": "60min"},
                {"time": "16:00", "task": "复习", "duration": "30min"}
            ]
        else:
            return [
                {"time": "09:00", "task": "算法学习", "duration": "60min"},
                {"time": "11:00", "task": "项目开发", "duration": "90min"},
                {"time": "14:00", "task": "代码审查", "duration": "60min"},
                {"time": "16:00", "task": "学习新技术", "duration": "60min"}
            ]


_planner = None

def get_study_planner() -> StudyPlanner:
    global _planner
    if _planner is None:
        _planner = StudyPlanner()
    return _planner


# 测试
if __name__ == "__main__":
    planner = get_study_planner()
    
    print("=== 学习计划测试 ===\n")
    
    week = planner.generate_week_plan()
    print("周计划:")
    for p in week:
        print(f"  {p['day']}: {p['topic']}")
    
    print("\n今日任务:")
    today = planner.get_today_task()
    print(f"  {today['task']}")

#!/usr/bin/env python3
"""
Planner Agent - 计划代理
"""
from typing import Dict, List


class PlannerAgent:
    """学习计划代理"""
    
    def generate_plan(self, level: str = "beginner") -> Dict:
        """生成学习计划"""
        
        if level == "beginner":
            plan = [
                {"day": "周一", "topic": "变量和数据类型", "task": "完成5道题"},
                {"day": "周二", "topic": "运算符", "task": "完成5道题"},
                {"day": "周三", "topic": "条件语句", "task": "完成3道题"},
                {"day": "周四", "topic": "循环", "task": "完成5道题"},
                {"day": "周五", "topic": "函数", "task": "完成小项目"},
                {"day": "周六", "topic": "综合练习", "task": "完成项目"},
                {"day": "周日", "topic": "复习", "task": "复习本周内容"}
            ]
        else:
            plan = [
                {"day": "周一", "topic": "算法", "task": "2道算法题"},
                {"day": "周二", "topic": "数据结构", "task": "1个项目"},
                {"day": "周三", "topic": "系统设计", "task": "设计题"},
                {"day": "周四", "topic": "代码审查", "task": "审查代码"},
                {"day": "周五", "topic": "项目", "task": "完成项目"},
                {"day": "周六", "topic": "挑战", "task": "参加竞技"},
                {"day": "周日", "topic": "总结", "task": "周总结"}
            ]
        
        return {
            "level": level,
            "plan": plan
        }


_agent = None

def get_planner_agent():
    global _agent
    if _agent is None:
        _agent = PlannerAgent()
    return _agent

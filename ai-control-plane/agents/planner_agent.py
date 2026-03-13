#!/usr/bin/env python3
"""
Planner Agent - 规划Agent
继承自BaseAgent
"""
from base_agent import BaseAgent


class PlannerAgent(BaseAgent):
    """Planner Agent - 规划者"""
    
    def __init__(self, router=None):
        super().__init__("Planner", "规划者", "qwen3.5:9b")
        self.router = router
    
    def plan(self, task: str) -> str:
        """制定计划"""
        self.tasks_completed += 1
        
        # 拆解任务
        steps = []
        steps.append("1. 理解任务需求")
        
        if "和" in task or "并且" in task:
            parts = task.split("和")
            for i, part in enumerate(parts, 2):
                steps.append(f"{i}. {part.strip()}")
        else:
            steps.append("2. 收集信息")
            steps.append("3. 执行任务")
            steps.append("4. 验证结果")
        
        return "[Planner] 计划:\n" + "\n".join(steps)
    
    def decompose(self, task: str) -> list:
        """拆解任务"""
        subtasks = []
        
        if "和" in task:
            parts = task.split("和")
            for part in parts:
                subtasks.append(part.strip())
        
        return subtasks


# 全局实例
_planner = None

def get_planner_agent(router=None) -> PlannerAgent:
    global _planner
    if _planner is None:
        _planner = PlannerAgent(router)
    return _planner

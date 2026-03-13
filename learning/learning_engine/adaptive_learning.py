#!/usr/bin/env python3
"""
Adaptive Learning - 自适应学习
根据用户水平自动调整难度
"""
from typing import Dict


class AdaptiveLearning:
    """自适应学习"""
    
    def __init__(self):
        self.user_level = "beginner"  # beginner/intermediate/advanced
        self.skills = {}  # 技能掌握程度
        self.difficulty = 1  # 1-10
    
    def assess_level(self, correct_rate: float):
        """评估水平"""
        if correct_rate >= 0.9:
            self.user_level = "advanced"
            self.difficulty = min(10, self.difficulty + 1)
        elif correct_rate >= 0.7:
            self.user_level = "intermediate"
        else:
            self.user_level = "beginner"
            self.difficulty = max(1, self.difficulty - 1)
        
        return self.user_level
    
    def get_difficulty(self) -> str:
        """获取推荐难度"""
        levels = {
            "beginner": "简单",
            "intermediate": "中等", 
            "advanced": "困难"
        }
        return levels.get(self.user_level, "简单")
    
    def recommend_topic(self) -> str:
        """推荐主题"""
        if self.user_level == "beginner":
            return ["变量", "循环", "函数"][self.difficulty % 3]
        elif self.user_level == "intermediate":
            return ["装饰器", "类", "模块"][self.difficulty % 3]
        else:
            return ["算法", "设计模式", "异步"][self.difficulty % 3]


_adaptive = None

def get_adaptive_learning() -> AdaptiveLearning:
    global _adaptive
    if _adaptive is None:
        _adaptive = AdaptiveLearning()
    return _adaptive

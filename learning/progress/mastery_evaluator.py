#!/usr/bin/env python3
"""
Mastery Evaluator - 掌握度评估
"""
from typing import Dict


class MasteryEvaluator:
    """掌握度评估"""
    
    def __init__(self):
        self.evaluations = {}
    
    def evaluate(self, skill: str, correct_rate: float, time_spent: int) -> Dict:
        """评估掌握度"""
        # 基于正确率和耗时
        if correct_rate >= 0.9 and time_spent < 300:
            level = "精通"
            mastery = 100
        elif correct_rate >= 0.8:
            level = "熟练"
            mastery = 80
        elif correct_rate >= 0.6:
            level = "掌握"
            mastery = 60
        elif correct_rate >= 0.4:
            level = "学习中"
            mastery = 40
        else:
            level = "入门"
            mastery = 20
        
        self.evaluations[skill] = {
            "level": level,
            "mastery": mastery,
            "correct_rate": correct_rate,
            "time_spent": time_spent
        }
        
        return {"level": level, "mastery": mastery}
    
    def get_mastery(self, skill: str) -> int:
        if skill in self.evaluations:
            return self.evaluations[skill]["mastery"]
        return 0
    
    def get_all(self) -> Dict:
        return self.evaluations


_evaluator = None

def get_mastery_evaluator() -> MasteryEvaluator:
    global _evaluator
    if _evaluator is None:
        _evaluator = MasteryEvaluator()
    return _evaluator

#!/usr/bin/env python3
"""
Weakness Detector - 弱点检测
"""
from typing import Dict, List


class WeaknessDetector:
    """弱点检测"""
    
    # 技能与错误映射
    WEAKNESS_MAP = {
        "语法错误": ["变量", "函数"],
        "逻辑错误": ["循环", "条件"],
        "性能问题": ["算法", "数据结构"],
        "设计问题": ["OOP", "架构"]
    }
    
    def __init__(self):
        self.error_history = []
    
    def add_error(self, error_type: str, skill: str):
        """添加错误记录"""
        self.error_history.append({
            "type": error_type,
            "skill": skill
        })
    
    def detect_weakness(self) -> List[Dict]:
        """检测弱点"""
        
        weaknesses = {}
        
        for error in self.error_history:
            skill = error.get("skill", "unknown")
            if skill not in weaknesses:
                weaknesses[skill] = 0
            weaknesses[skill] += 1
        
        # 排序
        sorted_weak = sorted(weaknesses.items(), key=lambda x: x[1], reverse=True)
        
        return [
            {"skill": s, "count": c, "advice": self._get_advice(s)}
            for s, c in sorted_weak[:3]
        ]
    
    def _get_advice(self, skill: str) -> str:
        advice = {
            "变量": "多练习变量赋值和类型转换",
            "函数": "学习函数定义和参数传递",
            "循环": "练习for和while循环",
            "条件": "熟悉if-elif-else结构",
            "算法": "学习基础算法和数据结构",
            "OOP": "学习类和对象的概念"
        }
        return advice.get(skill, "多加练习")


_detector = None

def get_weakness_detector():
    global _detector
    if _detector is None:
        _detector = WeaknessDetector()
    return _detector

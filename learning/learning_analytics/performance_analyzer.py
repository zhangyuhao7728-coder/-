#!/usr/bin/env python3
"""
Performance Analyzer - 性能分析
"""
from typing import Dict, List


class PerformanceAnalyzer:
    """学习性能分析"""
    
    def analyze(self, stats: Dict) -> Dict:
        """分析学习性能"""
        
        total_time = stats.get("total_time", 0)
        problems = stats.get("problems", 0)
        
        # 计算效率
        if total_time > 0:
            efficiency = problems / (total_time / 60)
        else:
            efficiency = 0
        
        # 评估
        if efficiency > 1:
            rating = "优秀"
        elif efficiency > 0.5:
            rating = "良好"
        else:
            rating = "需提高"
        
        return {
            "efficiency": round(efficiency, 2),
            "rating": rating,
            "suggestions": self._get_suggestions(efficiency)
        }
    
    def _get_suggestions(self, efficiency: float) -> List[str]:
        if efficiency > 1:
            return ["保持当前学习节奏", "可以尝试更高难度内容"]
        elif efficiency > 0.5:
            return ["增加练习量", "每天多刷一道题"]
        else:
            return ["增加学习时间", "先巩固基础知识"]


_analyzer = None

def get_performance_analyzer():
    global _analyzer
    if _analyzer is None:
        _analyzer = PerformanceAnalyzer()
    return _analyzer

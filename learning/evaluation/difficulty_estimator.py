#!/usr/bin/env python3
"""
Difficulty Estimator - 难度评估系统
自动评估题目难度
"""
import re
from typing import Dict


class DifficultyEstimator:
    """难度评估器"""
    
    # 关键词映射
    DIFFICULTY_KEYWORDS = {
        "easy": [
            "hello", "world", "print", "变量", "基础",
            "两数之和", "反转", "判断", "简单"
        ],
        "medium": [
            "循环", "遍历", "排序", "查找",
            "二分", "链表", "栈", "队列",
            "中等", "优化"
        ],
        "hard": [
            "动态规划", "dp", "递归",
            "图", "bfs", "dfs",
            "困难", "hard", "复杂"
        ]
    }
    
    def __init__(self):
        self.history = []
    
    def estimate(self, problem: str) -> str:
        """评估难度"""
        problem_lower = problem.lower()
        
        # 统计关键词
        easy_count = sum(1 for kw in self.DIFFICULTY_KEYWORDS["easy"] if kw in problem_lower)
        medium_count = sum(1 for kw in self.DIFFICULTY_KEYWORDS["medium"] if kw in problem_lower)
        hard_count = sum(1 for kw in self.DIFFICULTY_KEYWORDS["hard"] if kw in problem_lower)
        
        # 判断
        if hard_count > medium_count and hard_count > easy_count:
            return "hard"
        elif medium_count > easy_count:
            return "medium"
        else:
            return "easy"
    
    def estimate_score(self, problem: str) -> Dict:
        """评估并返回详细信息"""
        difficulty = self.estimate(problem)
        
        # 分数范围
        scores = {
            "easy": (1, 3),
            "medium": (4, 6),
            "hard": (7, 10)
        }
        
        return {
            "difficulty": difficulty,
            "score_range": scores.get(difficulty, (1, 10)),
            "reason": self._get_reason(problem)
        }
    
    def _get_reason(self, problem: str) -> str:
        problem_lower = problem.lower()
        
        if "动态规划" in problem or "dp" in problem_lower:
            return "涉及动态规划"
        elif "递归" in problem:
            return "涉及递归"
        elif "图" in problem:
            return "涉及图算法"
        elif "循环" in problem:
            return "涉及循环遍历"
        else:
            return "基础语法考察"
    
    # 根据表现调整
    def adjust_by_score(self, current: str, score: float) -> str:
        """根据得分调整难度"""
        if score >= 90:
            return "hard"
        elif score >= 70:
            return "medium"
        elif score >= 50:
            return current  # 保持
        else:
            return "easy"


# 全局实例
_estimator = None

def get_difficulty_estimator() -> DifficultyEstimator:
    global _estimator
    if _estimator is None:
        _estimator = DifficultyEstimator()
    return _estimator

def estimate(problem: str) -> str:
    return get_difficulty_estimator().estimate(problem)


# 测试
if __name__ == "__main__":
    est = get_difficulty_estimator()
    
    print("=== 难度评估测试 ===\n")
    
    problems = [
        "写一个Hello World",
        "实现二分查找",
        "动态规划最长公共子序列"
    ]
    
    for p in problems:
        result = est.estimate_score(p)
        print(f"{p}: {result['difficulty']}")

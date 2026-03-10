#!/usr/bin/env python3
"""
🎯 问题生成器
自动生成算法题目
"""

import random
import json
from pathlib import Path

class ProblemGenerator:
    def __init__(self):
        self.base_dir = Path("~/项目/Ai学习系统/learning/problems").expanduser()
        
        self.problem_templates = {
            "easy": {
                "数组": [
                    {"title": "两数之和", "template": "给定数组nums和目标值target,找出两数之和等于target的两个数的下标"},
                    {"title": "最大子数组和", "template": "找出连续子数组的最大和"},
                    {"title": "买卖股票最佳时机", "template": "计算买入卖出股票的最大利润"},
                ],
                "字符串": [
                    {"title": "回文数判断", "template": "判断一个整数是否为回文数"},
                    {"title": "反转字符串", "template": "反转字符串"},
                ],
                "链表": [
                    {"title": "删除链表节点", "template": "删除链表中值为val的节点"},
                ]
            },
            "medium": {
                "滑动窗口": [
                    {"title": "最大子数组和", "template": "找出长度不超过k的最大子数组和"},
                    {"title": "无重复字符最长子串", "template": "找出不重复字符的最长子串长度"},
                ],
                "动态规划": [
                    {"title": "爬楼梯", "template": "有n阶楼梯,每次爬1或2阶,有多少种方法"},
                    {"title": "最长递增子序列", "template": "找出最长递增子序列的长度"},
                ]
            }
        }
    
    def generate(self, difficulty="easy", topic=None):
        """生成题目"""
        if difficulty not in self.problem_templates:
            difficulty = "easy"
        
        topics = self.problem_templates[difficulty]
        
        if topic and topic in topics:
            problems = topics[topic]
        else:
            # 随机选择一个主题
            all_problems = []
            for t, probs in topics.items():
                all_problems.extend(probs)
            problems = all_problems
        
        problem = random.choice(problems)
        
        return {
            "difficulty": difficulty,
            "title": problem["title"],
            "description": problem["template"],
            "examples": self._generate_examples(problem["title"]),
            "constraints": self._generate_constraints(problem["title"]),
            "hints": self._generate_hints(problem["title"])
        }
    
    def _generate_examples(self, title):
        """生成示例"""
        examples = {
            "两数之和": {
                "input": "nums = [2,7,11,15], target = 9",
                "output": "[0,1]"
            },
            "最大子数组和": {
                "input": "nums = [-2,1,-3,4,-1,2,1,-5,4]",
                "output": "6"
            },
            "回文数判断": {
                "input": "x = 121",
                "output": "True"
            }
        }
        return examples.get(title, {"input": "...", "output": "..."})
    
    def _generate_constraints(self, title):
        """生成约束条件"""
        return [
            "1 <= nums.length <= 10^4",
            "-10^9 <= nums[i] <= 10^9"
        ]
    
    def _generate_hints(self, title):
        """生成提示"""
        hints = {
            "两数之和": ["可以使用哈希表来降低时间复杂度", "暴力解法是O(n²)"],
            "最大子数组和": ["考虑使用动态规划", "Kadane算法"],
            "回文数判断": ["可以转换为字符串", "也可以用数字反转"]
        }
        return hints.get(title, ["仔细分析问题"])

def main():
    generator = ProblemGenerator()
    
    print("🎯 问题生成器")
    print("=" * 40)
    
    # 生成一道简单题
    problem = generator.generate("easy")
    print(f"\n难度: {problem['difficulty']}")
    print(f"题目: {problem['title']}")
    print(f"描述: {problem['description']}")
    print(f"\n示例:")
    print(f"  输入: {problem['examples']['input']}")
    print(f"  输出: {problem['examples']['output']}")
    print(f"\n提示: {problem['hints'][0]}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Debugging Trainer - Debug训练
"""
import random
from typing import Dict, List


class DebuggingTrainer:
    """调试训练"""
    
    # 练习题
    BUG_EXERCISES = [
        {
            "id": "off_by_one",
            "title": " Off-by-one错误",
            "buggy_code": "for i in range(1, 10):\n    print(i)\n# 应该是0-9",
            "hint": "range范围是左闭右开",
            "solution": "range(10)"
        },
        {
            "id": "scope",
            "title": "作用域问题",
            "buggy_code": "x = 10\ndef foo():\n    x = x + 1\n    return x",
            "hint": "函数内使用全局变量需要global",
            "solution": "global x"
        },
        {
            "id": "mutable",
            "title": "可变默认参数",
            "buggy_code": "def add(item, list=[]):\n    list.append(item)\n    return list",
            "hint": "默认参数只计算一次",
            "solution": "list=None"
        },
        {
            "id": "closure",
            "title": "闭包延迟绑定",
            "buggy_code": "funcs = [lambda x: x+i for i in range(3)]\nprint(funcs[0](0))",
            "hint": "循环变量在调用时才读取",
            "solution": "lambda x, i=i: x+i"
        }
    ]
    
    def __init__(self):
        self.completed = []
        self.current = None
    
    def get_exercise(self, difficulty: str = "medium") -> Dict:
        """获取练习"""
        
        exercises = self.BUG_EXERCISES
        exercise = random.choice(exercises)
        
        self.current = exercise
        
        return exercise
    
    def check_solution(self, solution: str) -> Dict:
        """检查解答"""
        
        if not self.current:
            return {"error": "没有当前练习"}
        
        # 简单检查
        correct = solution.strip() == self.current["solution"].strip()
        
        if correct:
            self.completed.append(self.current["id"])
        
        return {
            "correct": correct,
            "hint": self.current["hint"] if not correct else "",
            "solution": self.current["solution"] if correct else ""
        }
    
    def get_all_exercises(self) -> List[Dict]:
        """获取所有练习"""
        return self.BUG_EXERCISES


_trainer = None

def get_debugging_trainer() -> DebuggingTrainer:
    global _trainer
    if _trainer is None:
        _trainer = DebuggingTrainer()
    return _trainer


# 测试
if __name__ == "__main__":
    trainer = get_debugging_trainer()
    
    print("=== Debug训练测试 ===\n")
    
    # 获取练习
    ex = trainer.get_exercise()
    print(f"练习: {ex['title']}")
    print(f"代码:\n{ex['buggy_code']}")
    print(f"提示: {ex['hint']}")

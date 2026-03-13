#!/usr/bin/env python3
"""
Bug Generator - Bug生成器
"""
import random
from typing import Dict, List


class BugGenerator:
    """Bug生成器"""
    
    # 带Bug的代码
    BUGGY_CODES = [
        {
            "id": "syntax_missing_colon",
            "title": "缺少冒号",
            "buggy": "def hello()\n    print('hello')",
            "error": "SyntaxError",
            "fix": "def hello():"
        },
        {
            "id": "indentation_error",
            "title": "缩进错误",
            "buggy": "if True:\nprint('hello')",
            "error": "IndentationError",
            "fix": "    print('hello')"
        },
        {
            "id": "undefined_variable",
            "title": "未定义变量",
            "buggy": "print(x)\nx = 1",
            "error": "NameError",
            "fix": "x = 1\nprint(x)"
        },
        {
            "id": "off_by_one",
            "title": "Off-by-one",
            "buggy": "for i in range(1, 10):\n    print(i)",
            "error": "LogicError",
            "fix": "for i in range(10):"
        },
        {
            "id": "mutable_default",
            "title": "可变默认参数",
            "buggy": "def add(item, list=[]):\n    list.append(item)\n    return list",
            "error": "LogicError",
            "fix": "def add(item, list=None):\n    if list is None:\n        list = []"
        },
        {
            "id": "string_concat",
            "title": "字符串拼接",
            "buggy": "s = ''\nfor i in range(10):\n    s += str(i)",
            "error": "Performance",
            "fix": "s = ''.join(str(i) for i in range(10))"
        },
        {
            "id": "division_by_zero",
            "title": "除零错误",
            "buggy": "def divide(a, b):\n    return a / b",
            "error": "ZeroDivisionError",
            "fix": "if b != 0: return a / b"
        },
        {
            "id": "wrong_comparison",
            "title": "比较运算符错误",
            "buggy": "if x = 5:\n    print(x)",
            "error": "SyntaxError",
            "fix": "if x == 5:"
        }
    ]
    
    def generate(self, difficulty: str = "medium") -> Dict:
        """生成Bug代码"""
        return random.choice(self.BUGGY_CODES)
    
    def get_all(self) -> List[Dict]:
        return self.BUGGY_CODES


_generator = None

def get_bug_generator():
    global _generator
    if _generator is None:
        _generator = BugGenerator()
    return _generator

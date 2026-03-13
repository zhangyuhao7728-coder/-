#!/usr/bin/env python3
"""
Mistakes Tracker - 错误记录
"""
import json
from datetime import datetime
from typing import List, Dict


class MistakesTracker:
    """错误记录"""
    
    def __init__(self):
        self.data_file = "/Users/zhangyuhao/项目/Ai学习系统/learning/knowledge-base/mistakes/mistakes.json"
        self.load()
    
    def load(self):
        try:
            with open(self.data_file) as f:
                self.data = json.load(f)
        except:
            self.data = {
                "mistakes": [],
                "categories": {}
            }
    
    def save(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def add(self, mistake: str, error_code: str, solution: str, category: str = "语法"):
        """添加错误"""
        
        entry = {
            "mistake": mistake,
            "error_code": error_code,
            "solution": solution,
            "category": category,
            "count": 1,
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        
        self.data["mistakes"].append(entry)
        
        # 分类统计
        if category not in self.data["categories"]:
            self.data["categories"][category] = 0
        self.data["categories"][category] += 1
        
        self.save()
    
    def get_all(self) -> List[Dict]:
        """获取所有错误"""
        return self.data["mistakes"]
    
    def get_by_category(self, category: str) -> List[Dict]:
        """按分类获取"""
        return [m for m in self.data["mistakes"] if m.get("category") == category]
    
    def get_common(self, n: int = 5) -> List[Dict]:
        """获取常见错误"""
        return self.data["mistakes"][-n:]


# 常见错误
COMMON_MISTAKES = [
    {
        "mistake": "缩进错误",
        "error_code": "IndentationError",
        "solution": "检查代码缩进，保持一致",
        "category": "语法"
    },
    {
        "mistake": "变量未定义",
        "error_code": "NameError",
        "solution": "检查变量名拼写",
        "category": "语法"
    },
    {
        "mistake": "索引越界",
        "error_code": "IndexError",
        "solution": "检查索引范围",
        "category": "逻辑"
    },
    {
        "mistake": "类型不匹配",
        "error_code": "TypeError",
        "solution": "检查数据类型",
        "category": "类型"
    },
    {
        "mistake": "除零错误",
        "error_code": "ZeroDivisionError",
        "solution": "检查除数是否为零",
        "category": "逻辑"
    }
]


def init_common_mistakes():
    """初始化常见错误"""
    tracker = MistakesTracker()
    
    # 只添加不存在的
    existing = [m["error_code"] for m in tracker.get_all()]
    
    for mistake in COMMON_MISTAKES:
        if mistake["error_code"] not in existing:
            tracker.add(**mistake)


_tracker = None

def get_mistakes_tracker() -> MistakesTracker:
    global _tracker
    if _tracker is None:
        _tracker = MistakesTracker()
    return _tracker


# 测试
if __name__ == "__main__":
    tracker = get_mistakes_tracker()
    
    print("=== 错误记录测试 ===\n")
    
    # 初始化
    init_common_mistakes()
    
    # 常见错误
    print("常见错误:")
    for m in tracker.get_common():
        print(f"  - {m['mistake']}: {m['solution']}")

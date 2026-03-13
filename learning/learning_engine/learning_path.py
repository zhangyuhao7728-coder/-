#!/usr/bin/env python3
"""
Learning Path - 完整学习路径
"""
from typing import Dict, List


class LearningPath:
    """学习路径引擎"""
    
    # 完整学习路径
    LEARNING_PATHS = [
        {
            "id": "python-basics",
            "name": "Python基础",
            "duration": "4周",
            "difficulty": 1,
            "steps": [
                {"week": 1, "topic": "变量和数据类型", "status": "pending"},
                {"week": 1, "topic": "运算符", "status": "pending"},
                {"week": 2, "topic": "条件语句if/else", "status": "pending"},
                {"week": 2, "topic": "循环for/while", "status": "pending"},
                {"week": 3, "topic": "函数def", "status": "pending"},
                {"week": 3, "topic": "模块和包import", "status": "pending"},
                {"week": 4, "topic": "列表list操作", "status": "pending"},
                {"week": 4, "topic": "字典dict操作", "status": "pending"},
            ]
        },
        {
            "id": "python-advanced",
            "name": "Python进阶",
            "duration": "4周",
            "difficulty": 3,
            "steps": [
                {"week": 1, "topic": "装饰器decorator", "status": "pending"},
                {"week": 1, "topic": "生成器yield", "status": "pending"},
                {"week": 2, "topic": "异步编程async/await", "status": "pending"},
                {"week": 2, "topic": "多进程multiprocessing", "status": "pending"},
                {"week": 3, "topic": "面向对象OOP", "status": "pending"},
                {"week": 3, "topic": "异常处理try/except", "status": "pending"},
                {"week": 4, "topic": "文件操作", "status": "pending"},
                {"week": 4, "topic": "性能优化", "status": "pending"},
            ]
        },
        {
            "id": "algorithms",
            "name": "算法与数据结构",
            "duration": "4周",
            "difficulty": 5,
            "steps": [
                {"week": 1, "topic": "数组和字符串", "status": "pending"},
                {"week": 1, "topic": "链表", "status": "pending"},
                {"week": 2, "topic": "栈和队列", "status": "pending"},
                {"week": 2, "topic": "哈希表", "status": "pending"},
                {"week": 3, "topic": "树和二叉树", "status": "pending"},
                {"week": 3, "topic": "图和BFS/DFS", "status": "pending"},
                {"week": 4, "topic": "动态规划", "status": "pending"},
                {"week": 4, "topic": "贪心和分治", "status": "pending"},
            ]
        },
        {
            "id": "ai-ml",
            "name": "AI/ML入门",
            "duration": "4周",
            "difficulty": 6,
            "steps": [
                {"week": 1, "topic": "NumPy数组操作", "status": "pending"},
                {"week": 1, "topic": "Pandas数据处理", "status": "pending"},
                {"week": 2, "topic": "Matplotlib可视化", "status": "pending"},
                {"week": 2, "topic": "sklearn机器学习基础", "status": "pending"},
                {"week": 3, "topic": "线性回归", "status": "pending"},
                {"week": 3, "topic": "分类算法", "status": "pending"},
                {"week": 4, "topic": "PyTorch基础", "status": "pending"},
                {"week": 4, "topic": "神经网络入门", "status": "pending"},
            ]
        },
        {
            "id": "data-skills",
            "name": "数据技能",
            "duration": "3周",
            "difficulty": 4,
            "steps": [
                {"week": 1, "topic": "数据清洗", "status": "pending"},
                {"week": 1, "topic": "数据探索EDA", "status": "pending"},
                {"week": 2, "topic": "特征工程", "status": "pending"},
                {"week": 2, "topic": "统计学基础", "status": "pending"},
                {"week": 3, "topic": "SQL查询", "status": "pending"},
                {"week": 3, "topic": "大数据入门", "status": "pending"},
            ]
        }
    ]
    
    def __init__(self):
        self.paths = self.LEARNING_PATHS
        self.current_path_id = None
        self.current_step = 0
    
    def get_all_paths(self) -> List[Dict]:
        """获取所有学习路径"""
        return self.paths
    
    def get_path(self, path_id: str) -> Dict:
        """获取指定路径"""
        for path in self.paths:
            if path["id"] == path_id:
                return path
        return {}
    
    def get_current(self) -> Dict:
        """获取当前路径"""
        if self.current_path_id:
            return self.get_path(self.current_path_id)
        return self.paths[0] if self.paths else {}
    
    def set_current(self, path_id: str):
        """设置当前路径"""
        self.current_path_id = path_id
        self.current_step = 0
    
    def next_step(self) -> Dict:
        """下一步"""
        path = self.get_current()
        steps = path.get("steps", [])
        
        if self.current_step < len(steps):
            step = steps[self.current_step]
            self.current_step += 1
            return step
        
        return {}
    
    def get_progress(self) -> float:
        """获取进度"""
        path = self.get_current()
        steps = path.get("steps", [])
        
        if not steps:
            return 0
        
        completed = sum(1 for s in steps if s.get("status") == "completed")
        return (completed / len(steps)) * 100
    
    def complete_step(self, step_topic: str):
        """完成步骤"""
        path = self.get_current()
        steps = path.get("steps", [])
        
        for step in steps:
            if step["topic"] == step_topic:
                step["status"] = "completed"


_path = None

def get_learning_path() -> LearningPath:
    global _path
    if _path is None:
        _path = LearningPath()
    return _path

#!/usr/bin/env python3
"""
Experiment Tasks - 实验任务
"""
from typing import Dict, List
from code_runner import get_code_runner


class ExperimentTasks:
    """实验任务"""
    
    # 预设实验
    EXPERIMENTS = {
        "hello": {
            "title": "Hello World",
            "description": "输出Hello World",
            "code": "print('Hello World')",
            "expected": "Hello World"
        },
        "variables": {
            "title": "变量实验",
            "description": "学习变量赋值",
            "code": "x = 5\ny = 3\nprint(x + y)",
            "expected": "8"
        },
        "list": {
            "title": "列表实验",
            "description": "列表操作",
            "code": "nums = [1, 2, 3]\nprint(sum(nums))",
            "expected": "6"
        },
        "loop": {
            "title": "循环实验",
            "description": "for循环",
            "code": "for i in range(5):\n    print(i, end=' ')",
            "expected": "0 1 2 3 4"
        },
        "function": {
            "title": "函数实验",
            "description": "定义函数",
            "code": "def add(a, b):\n    return a + b\nprint(add(2, 3))",
            "expected": "5"
        },
        "dict": {
            "title": "字典实验",
            "description": "字典操作",
            "code": "d = {'a': 1, 'b': 2}\nprint(d.get('a'))",
            "expected": "1"
        }
    }
    
    def __init__(self):
        self.runner = get_code_runner()
        self.completed = []
    
    def get_task(self, name: str) -> Dict:
        """获取任务"""
        return self.EXPERIMENTS.get(name, {})
    
    def run_task(self, name: str) -> Dict:
        """运行任务"""
        
        task = self.get_task(name)
        if not task:
            return {"error": "任务不存在"}
        
        code = task.get("code", "")
        expected = task.get("expected", "")
        
        result = self.runner.run_test(code, expected)
        
        if result["passed"]:
            self.completed.append(name)
        
        return {
            "task": task,
            "result": result
        }
    
    def get_all_tasks(self) -> List[Dict]:
        """获取所有任务"""
        
        tasks = []
        for name, info in self.EXPERIMENTS.items():
            tasks.append({
                "name": name,
                "title": info["title"],
                "description": info["description"],
                "completed": name in self.completed
            })
        
        return tasks
    
    def run_all(self) -> Dict:
        """运行所有任务"""
        
        results = []
        passed = 0
        
        for name in self.EXPERIMENTS:
            result = self.run_task(name)
            if result.get("result", {}).get("passed"):
                passed += 1
            results.append(result)
        
        return {
            "total": len(self.EXPERIMENTS),
            "passed": passed,
            "results": results
        }


_tasks = None

def get_experiment_tasks() -> ExperimentTasks:
    global _tasks
    if _tasks is None:
        _tasks = ExperimentTasks()
    return _tasks


# 测试
if __name__ == "__main__":
    tasks = get_experiment_tasks()
    
    print("=== 实验任务测试 ===\n")
    
    # 查看任务
    for task in tasks.get_all_tasks():
        status = "✅" if task["completed"] else "⏳"
        print(f"{status} {task['title']}: {task['description']}")
    
    # 运行
    print("\n运行结果:")
    result = tasks.run_task("hello")
    print(f"Hello: {result['result']['passed']}")

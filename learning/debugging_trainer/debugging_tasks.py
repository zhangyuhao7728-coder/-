#!/usr/bin/env python3
"""
Debugging Tasks - 调试任务
"""
from typing import Dict, List


class DebuggingTasks:
    """调试任务"""
    
    TASKS = [
        {
            "id": "find_bug_1",
            "title": "找出循环Bug",
            "description": "这个循环有什么问题?",
            "code": "for i in range(1, 5):\n    print(i)",
            "hint": "range的范围",
            "answer": "range(5)"
        },
        {
            "id": "find_bug_2",
            "title": "找出变量作用域Bug",
            "description": "为什么函数报错?",
            "code": "x = 10\ndef foo():\n    x = x + 1\n    return x",
            "hint": "global关键字",
            "answer": "global x"
        },
        {
            "id": "find_bug_3",
            "title": "找出列表Bug",
            "description": "列表操作有问题",
            "code": "nums = [1, 2, 3]\nprint(nums[5])",
            "hint": "索引范围",
            "answer": "nums[2]"
        }
    ]
    
    def get_task(self, task_id: str = None) -> Dict:
        """获取任务"""
        if task_id:
            for task in self.TASKS:
                if task["id"] == task_id:
                    return task
        return self.TASKS[0]
    
    def get_all(self) -> List[Dict]:
        return self.TASKS
    
    def check_answer(self, task_id: str, answer: str) -> bool:
        """检查答案"""
        task = self.get_task(task_id)
        return answer.strip() == task["answer"].strip()


_tasks = None

def get_debugging_tasks():
    global _tasks
    if _tasks is None:
        _tasks = DebuggingTasks()
    return _tasks

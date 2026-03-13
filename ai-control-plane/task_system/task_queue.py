#!/usr/bin/env python3
"""
Task Queue - 任务队列
"""
from collections import deque
from typing import Dict, List, Optional


class TaskQueue:
    """任务队列"""
    
    def __init__(self):
        self.queue = deque()
        self.priority_queue = deque()
    
    def add(self, task: Dict, priority: int = 0):
        """添加任务"""
        task["priority"] = priority
        
        if priority > 0:
            self.priority_queue.append(task)
        else:
            self.queue.append(task)
    
    def get(self) -> Optional[Dict]:
        """获取任务"""
        # 优先队列优先
        if self.priority_queue:
            return self.priority_queue.popleft()
        if self.queue:
            return self.queue.popleft()
        return None
    
    def size(self) -> int:
        return len(self.queue) + len(self.priority_queue)
    
    def clear(self):
        self.queue.clear()
        self.priority_queue.clear()


# 全局实例
_queue = None

def get_task_queue() -> TaskQueue:
    global _queue
    if _queue is None:
        _queue = TaskQueue()
    return _queue

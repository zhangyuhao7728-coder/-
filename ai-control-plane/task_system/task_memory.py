#!/usr/bin/env python3
"""
Task Memory - 任务记忆
"""
import json
from datetime import datetime
from typing import Dict, List


class TaskMemory:
    """任务记忆"""
    
    def __init__(self, max_size: int = 100):
        self.max_size = max_size
        self.memory = []
    
    def add(self, task: Dict):
        """添加记忆"""
        task["timestamp"] = datetime.now().isoformat()
        self.memory.append(task)
        
        if len(self.memory) > self.max_size:
            self.memory.pop(0)
    
    def search(self, keyword: str) -> List[Dict]:
        """搜索记忆"""
        results = []
        for m in self.memory:
            if keyword in str(m.get("prompt", "")):
                results.append(m)
        return results
    
    def get_recent(self, n: int = 10) -> List[Dict]:
        """获取最近N条"""
        return self.memory[-n:]
    
    def clear(self):
        self.memory.clear()
    
    def save(self, filepath: str):
        with open(filepath, 'w') as f:
            json.dump(self.memory, f, indent=2)


# 全局实例
_memory = None

def get_task_memory() -> TaskMemory:
    global _memory
    if _memory is None:
        _memory = TaskMemory()
    return _memory

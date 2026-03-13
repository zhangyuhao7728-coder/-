#!/usr/bin/env python3
"""
Task Manager - 任务管理器
功能：
1. 任务队列
2. 任务拆解
3. 任务调度
"""
from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum


class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class Task:
    """任务"""
    
    def __init__(self, id: str, prompt: str, task_type: str = "general"):
        self.id = id
        self.prompt = prompt
        self.task_type = task_type
        self.status = TaskStatus.PENDING
        self.result = None
        self.subtasks = []
        self.created_at = datetime.now()
        self.completed_at = None
        self.agent = None
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "prompt": self.prompt,
            "task_type": self.task_type,
            "status": self.status.value,
            "result": self.result,
            "subtasks": len(self.subtasks),
            "agent": self.agent,
            "created_at": self.created_at.isoformat(),
        }


class TaskManager:
    """任务管理器"""
    
    def __init__(self):
        self.tasks = {}
        self.queue = []
        self.task_id_counter = 0
    
    def create_task(self, prompt: str, task_type: str = "general") -> str:
        """创建任务"""
        self.task_id_counter += 1
        task_id = f"task_{self.task_id_counter}"
        
        task = Task(task_id, prompt, task_type)
        self.tasks[task_id] = task
        self.queue.append(task_id)
        
        return task_id
    
    def decompose_task(self, task_id: str) -> List[str]:
        """拆解任务"""
        task = self.tasks.get(task_id)
        if not task:
            return []
        
        prompt = task.prompt.lower()
        subtasks = []
        
        # 简单拆解逻辑
        if "和" in task.prompt or "并且" in task.prompt:
            # 多步骤任务
            parts = task.prompt.split("和")
            for i, part in enumerate(parts):
                part = part.strip()
                if part:
                    sub_id = f"{task_id}_sub_{i}"
                    subtasks.append(sub_id)
                    self.tasks[sub_id] = Task(sub_id, part, task.task_type)
            
            task.subtasks = subtasks
        
        return subtasks
    
    def get_task(self, task_id: str) -> Optional[Task]:
        return self.tasks.get(task_id)
    
    def get_next_task(self) -> Optional[str]:
        """获取下一个任务"""
        for task_id in self.queue:
            task = self.tasks.get(task_id)
            if task and task.status == TaskStatus.PENDING:
                return task_id
        return None
    
    def complete_task(self, task_id: str, result: str):
        """完成任务"""
        task = self.tasks.get(task_id)
        if task:
            task.status = TaskStatus.COMPLETED
            task.result = result
            task.completed_at = datetime.now()
            
            # 从队列移除
            if task_id in self.queue:
                self.queue.remove(task_id)
    
    def fail_task(self, task_id: str, error: str):
        """任务失败"""
        task = self.tasks.get(task_id)
        if task:
            task.status = TaskStatus.FAILED
            task.result = f"Error: {error}"
            task.completed_at = datetime.now()
            
            if task_id in self.queue:
                self.queue.remove(task_id)
    
    def get_status(self) -> Dict:
        """获取状态"""
        status = {
            "total": len(self.tasks),
            "pending": sum(1 for t in self.tasks.values() if t.status == TaskStatus.PENDING),
            "running": sum(1 for t in self.tasks.values() if t.status == TaskStatus.RUNNING),
            "completed": sum(1 for t in self.tasks.values() if t.status == TaskStatus.COMPLETED),
            "failed": sum(1 for t in self.tasks.values() if t.status == TaskStatus.FAILED),
        }
        return status
    
    def print_status(self):
        """打印状态"""
        s = self.get_status()
        print(f"=== Task Manager ===")
        print(f"总任务: {s['total']}")
        print(f"待处理: {s['pending']}")
        print(f"进行中: {s['running']}")
        print(f"已完成: {s['completed']}")
        print(f"失败: {s['failed']}")


# 全局实例
_manager = None

def get_task_manager() -> TaskManager:
    global _manager
    if _manager is None:
        _manager = TaskManager()
    return _manager


# 测试
if __name__ == "__main__":
    mgr = get_task_manager()
    
    print("=== Task Manager 测试 ===\n")
    
    # 创建任务
    task_id = mgr.create_task("写一个Python函数并测试它", "code")
    print(f"创建任务: {task_id}")
    
    # 拆解任务
    subtasks = mgr.decompose_task(task_id)
    print(f"拆解: {subtasks}")
    
    # 状态
    mgr.print_status()

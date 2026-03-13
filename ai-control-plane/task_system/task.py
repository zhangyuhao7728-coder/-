#!/usr/bin/env python3
"""
Task - 任务类
任务数据结构
"""
from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum


class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"
    PLANNING = "planning"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class Task:
    """任务"""
    
    def __init__(self, goal: str, task_id: str = None):
        self.id = task_id or f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.goal = goal  # 任务目标
        self.subtasks = []  # 子任务列表
        self.status = TaskStatus.PENDING
        self.result = None
        self.created_at = datetime.now()
        self.completed_at = None
        self.context = {}
    
    def add_subtask(self, subtask: 'SubTask'):
        """添加子任务"""
        self.subtasks.append(subtask)
    
    def set_status(self, status: TaskStatus):
        """设置状态"""
        self.status = status
    
    def complete(self, result: str):
        """完成任务"""
        self.status = TaskStatus.COMPLETED
        self.result = result
        self.completed_at = datetime.now()
    
    def fail(self, error: str):
        """任务失败"""
        self.status = TaskStatus.FAILED
        self.result = f"Error: {error}"
        self.completed_at = datetime.now()
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "goal": self.goal,
            "status": self.status.value,
            "subtasks": [s.to_dict() for s in self.subtasks],
            "result": self.result,
            "created_at": self.created_at.isoformat(),
        }


class SubTask:
    """子任务"""
    
    def __init__(self, description: str, agent_type: str = "general"):
        self.id = f"sub_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        self.description = description
        self.agent_type = agent_type  # coder, researcher, planner等
        self.status = TaskStatus.PENDING
        self.result = None
    
    def complete(self, result: str):
        self.status = TaskStatus.COMPLETED
        self.result = result
    
    def fail(self, error: str):
        self.status = TaskStatus.FAILED
        self.result = f"Error: {error}"
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "description": self.description,
            "agent_type": self.agent_type,
            "status": self.status.value,
            "result": self.result,
        }


# 测试
if __name__ == "__main__":
    print("=== Task 测试 ===\n")
    
    # 创建任务
    task = Task("写一个网页爬虫")
    print(f"任务: {task.goal}")
    print(f"状态: {task.status.value}")
    
    # 添加子任务
    task.add_subtask(SubTask("研究网站结构", "researcher"))
    task.add_subtask(SubTask("编写爬虫代码", "coder"))
    task.add_subtask(SubTask("测试爬虫", "tester"))
    task.add_subtask(SubTask("优化性能", "analyst"))
    
    print(f"\n子任务 ({len(task.subtasks)}):")
    for st in task.subtasks:
        print(f"  - {st.description} ({st.agent_type})")

#!/usr/bin/env python3
"""
Tasks - 任务定义
"""

from typing import Dict, Any, Optional, List
from enum import Enum
from pydantic import BaseModel
from datetime import datetime

class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"

class TaskAction(str, Enum):
    VISIT = "visit"
    SCREENSHOT = "screenshot"
    FILL = "fill"
    CLICK = "click"
    EVALUATE = "evaluate"

class Task(BaseModel):
    """任务模型"""
    id: str
    url: str
    action: TaskAction = TaskAction.VISIT
    selector: Optional[str] = None
    value: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    created_at: str = ""
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    
    def start(self):
        self.status = TaskStatus.RUNNING
        self.started_at = datetime.now().isoformat()
        
    def complete(self, result: Dict[str, Any]):
        self.status = TaskStatus.SUCCESS
        self.completed_at = datetime.now().isoformat()
        self.result = result
        
    def fail(self, error: str):
        self.status = TaskStatus.FAILED
        self.completed_at = datetime.now().isoformat()
        self.error = error


class TaskQueue:
    """任务队列"""
    
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.pending: List[str] = []
        self.running: List[str] = []
        self.completed: List[str] = []
        self.failed: List[str] = []
        
    def add(self, task: Task):
        self.tasks[task.id] = task
        self.pending.append(task.id)
        
    def get_next(self) -> Optional[Task]:
        if self.pending:
            task_id = self.pending.pop(0)
            self.running.append(task_id)
            return self.tasks[task_id]
        return None
        
    def complete(self, task_id: str, result: Dict[str, Any]):
        if task_id in self.running:
            self.running.remove(task_id)
        self.tasks[task_id].complete(result)
        self.completed.append(task_id)
        
    def fail(self, task_id: str, error: str):
        if task_id in self.running:
            self.running.remove(task_id)
        self.tasks[task_id].fail(error)
        self.failed.append(task_id)
        
    def status(self) -> dict:
        return {
            "pending": len(self.pending),
            "running": len(self.running),
            "completed": len(self.completed),
            "failed": len(self.failed),
            "total": len(self.tasks)
        }

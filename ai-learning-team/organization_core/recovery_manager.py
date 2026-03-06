"""
Recovery Manager
崩溃恢复管理器

负责在系统启动时扫描并恢复未完成的任务
"""

from typing import List, Dict, Any
from organization_core.task_queue import TaskQueue
from organization_core.persistence.task_repository import TaskRepository


class RecoveryManager:
    """
    崩溃恢复管理器
    
    启动时自动扫描并恢复 PENDING/RUNNING 状态的任务
    执行模型: At-Least-Once (至少一次，可能重复)
    """
    
    def __init__(self, task_queue: TaskQueue, repo: TaskRepository):
        self.task_queue = task_queue
        self.repo = repo
    
    def recover(self) -> Dict[str, Any]:
        """
        执行崩溃恢复
        
        扫描所有 PENDING 和 RUNNING 任务，重新入队执行
        
        Returns:
            恢复结果统计
        """
        # 1. 获取所有未完成任务
        unfinished_tasks = self.repo.get_unfinished_tasks()
        
        if not unfinished_tasks:
            print("✅ No tasks to recover")
            return {
                "found": 0,
                "recovered": 0,
                "failed": 0
            }
        
        print(f"🔄 Found {len(unfinished_tasks)} unfinished tasks")
        
        recovered = 0
        failed = 0
        
        # 2. 逐个恢复任务
        for task in unfinished_tasks:
            task_id = task["id"]
            content = task["content"]
            agent = task["agent"]
            current_status = task["status"]
            
            print(f"♻️ Recovering task #{task_id}: {agent} - {content[:30]}...")
            
            try:
                # 3. 重置任务状态为 PENDING
                self.repo.update_status(task_id, "PENDING")
                
                # 4. 重新入队
                self.task_queue.enqueue_existing(
                    task_id=task_id,
                    content=content,
                    agent_name=agent
                )
                
                recovered += 1
                print(f"   ✅ Task #{task_id} re-queued")
                
            except Exception as e:
                failed += 1
                print(f"   ❌ Task #{task_id} recovery failed: {e}")
        
        # 5. 返回统计
        result = {
            "found": len(unfinished_tasks),
            "recovered": recovered,
            "failed": failed,
            "status": "completed"
        }
        
        print(f"📊 Recovery complete: {recovered} recovered, {failed} failed")
        
        return result
    
    def get_unfinished_count(self) -> int:
        """获取未完成任务数量"""
        return len(self.repo.get_unfinished_tasks())
    
    def reset_all_running(self) -> int:
        """
        重置所有 RUNNING 状态的任务（用于手动恢复）
        
        Returns:
            重置的任务数量
        """
        running_tasks = self.repo.get_running()
        
        for task in running_tasks:
            self.repo.update_status(task["id"], "PENDING")
        
        return len(running_tasks)
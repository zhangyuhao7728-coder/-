"""
Task Queue
任务队列 - 异步任务调度 (带限流和并发控制)
"""

import json
import threading
from typing import Optional, Callable, Any, Dict
from organization_core.worker_pool import WorkerPool
from organization_core.persistence.task_repository import TaskRepository
from organization_core.agent_registry import AgentRegistry


# 队列配置
MAX_QUEUE_SIZE = 100  # 最大队列长度
MAX_AGENT_CONCURRENT = 2  # 单个 Agent 最大并发数


class TaskQueue:
    """任务队列 - 带限流和并发控制"""
    
    def __init__(self, registry: AgentRegistry, max_workers: int = 4):
        self.registry = registry
        self.worker_pool = WorkerPool(max_workers=max_workers)
        self.repo = TaskRepository()
        
        # 队列大小计数器
        self._queue_lock = threading.Lock()
        self._pending_count = 0
        
        # Agent 并发计数器
        self._agent_concurrent = {}  # {agent: count}
        self._agent_lock = threading.Lock()
        
        print(f"✅ TaskQueue initialized (max_workers={max_workers}, max_queue={MAX_QUEUE_SIZE}, max_agent_concurrent={MAX_AGENT_CONCURRENT})")
    
    def enqueue(self, content: str, agent_name: str, metadata: Optional[Dict] = None) -> int:
        """
        入队任务 (带限流)
        
        Args:
            content: 任务内容
            agent_name: Agent 名称
            metadata: 附加元数据
            
        Returns:
            task_id: 任务 ID
            
        Raises:
            ValueError: 队列满或 Agent 并发超限
        """
        # 1. 检查队列大小
        with self._queue_lock:
            if self._pending_count >= MAX_QUEUE_SIZE:
                raise ValueError(f"SYSTEM_BUSY: Queue full ({MAX_QUEUE_SIZE})")
        
        # 2. 检查 Agent 并发限制
        with self._agent_lock:
            current = self._agent_concurrent.get(agent_name, 0)
            if current >= MAX_AGENT_CONCURRENT:
                raise ValueError(f"AGENT_BUSY: {agent_name} concurrent limit ({MAX_AGENT_CONCURRENT})")
            self._agent_concurrent[agent_name] = current + 1
        
        # 3. 检查 Agent 是否存在
        if not self.registry.has(agent_name):
            with self._agent_lock:
                self._agent_concurrent[agent_name] = max(0, self._agent_concurrent.get(agent_name, 0) - 1)
            raise ValueError(f"Agent '{agent_name}' not registered")
        
        # 4. 创建任务记录
        task_id = self.repo.create(content, agent_name)
        
        # 5. 增加队列计数
        with self._queue_lock:
            self._pending_count += 1
        
        # 6. 提交到线程池
        self.worker_pool.submit(
            self._execute_task,
            task_id,
            content,
            agent_name,
            metadata
        )
        
        return task_id
    
    def _execute_task(
        self, 
        task_id: int, 
        content: str, 
        agent_name: str,
        metadata: Optional[Dict] = None
    ) -> None:
        """执行任务"""
        try:
            # 更新状态为 RUNNING
            self.repo.update_status(task_id, "RUNNING")
            
            print(f"🔄 [Task #{task_id}] {agent_name} processing: {content[:50]}...")
            
            # 获取 Agent
            agent = self.registry.get(agent_name)
            
            # 构建消息
            message = {
                "content": content,
                "task_id": task_id,
                "agent": agent_name
            }
            if metadata:
                message.update(metadata)
            
            # 执行 Agent
            result = agent(message)
            
            # 序列化结果
            if isinstance(result, dict):
                result_str = json.dumps(result, ensure_ascii=False, indent=2)
            else:
                result_str = str(result)
            
            # 更新状态为 SUCCESS
            self.repo.update_status(task_id, "SUCCESS", result=result_str)
            
            print(f"✅ [Task #{task_id}] {agent_name} completed")
            
        except Exception as e:
            # 更新状态为 FAILED
            self.repo.update_status(task_id, "FAILED", error=str(e))
            print(f"❌ [Task #{task_id}] {agent_name} failed: {e}")
        
        finally:
            # 减少队列计数
            with self._queue_lock:
                self._pending_count = max(0, self._pending_count - 1)
            
            # 减少 Agent 并发计数
            with self._agent_lock:
                self._agent_concurrent[agent_name] = max(0, self._agent_concurrent.get(agent_name, 1) - 1)
    
    def get_task(self, task_id: int) -> Optional[Dict]:
        """获取任务状态"""
        return self.repo.get(task_id)
    
    def list_tasks(self, status: Optional[str] = None, limit: int = 100) -> list:
        """列出任务"""
        if status:
            return self.repo.list_by_status(status, limit)
        return self.repo.list_all(limit)
    
    def get_stats(self) -> Dict:
        """获取队列统计"""
        all_tasks = self.repo.list_all(1000)
        
        stats = {
            "total": len(all_tasks),
            "PENDING": 0,
            "RUNNING": 0,
            "SUCCESS": 0,
            "FAILED": 0,
            "queue_size": self._pending_count,
            "max_queue": MAX_QUEUE_SIZE,
            "active_workers": self.worker_pool.get_active_count()
        }
        
        for task in all_tasks:
            task_status = task.get("status", "UNKNOWN")
            if task_status in stats:
                stats[task_status] += 1
        
        # Agent 并发状态
        with self._agent_lock:
            stats["agent_concurrent"] = self._agent_concurrent.copy()
        
        return stats
    
    def shutdown(self) -> None:
        """关闭任务队列"""
        self.worker_pool.shutdown()
    
    def enqueue_existing(self, task_id: int, content: str, agent_name: str, metadata: Optional[Dict] = None) -> None:
        """
        重新入队已存在的任务（用于崩溃恢复）
        """
        self.worker_pool.submit(
            self._execute_task,
            task_id,
            content,
            agent_name,
            metadata,
            task_id=task_id
        )

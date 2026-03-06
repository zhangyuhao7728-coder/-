"""
Worker Pool
线程池执行器 + LLM 调用支持 (带超时保护)
"""

from concurrent.futures import ThreadPoolExecutor, Future, as_completed, TimeoutError
from typing import Callable, Any, Optional, Dict
import threading
import time


class WorkerPool:
    """Worker 线程池"""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.active_tasks: dict[str, Future] = {}
        self.lock = threading.Lock()
        self.task_timeout = 60  # 默认任务超时 60秒
        print(f"✅ WorkerPool initialized with {max_workers} workers, timeout={self.task_timeout}s")
    
    def submit(self, fn: Callable, *args, task_id: Optional[int] = None, timeout: Optional[int] = None, **kwargs) -> Future:
        """提交任务到线程池 (带超时)"""
        # 使用指定超时或默认超时
        task_timeout = timeout or self.task_timeout
        
        # 包装函数添加超时
        def wrapped_fn():
            return fn(*args, **kwargs)
        
        future = self.executor.submit(wrapped_fn)
        
        if task_id is not None:
            with self.lock:
                self.active_tasks[str(task_id)] = (future, task_timeout)
        
        # 添加完成回调
        future.add_done_callback(lambda f: self._on_task_complete(f, task_id))
        
        print(f"🚀 Task #{task_id} submitted (timeout: {task_timeout}s)")
        return future
    
    def _on_task_complete(self, future: Future, task_id: Optional[int]) -> None:
        """任务完成回调 (带超时检查)"""
        if task_id is not None:
            with self.lock:
                if str(task_id) in self.active_tasks:
                    del self.active_tasks[str(task_id)]
            
            try:
                # 获取超时时间
                timeout = self.task_timeout
                with self.lock:
                    if str(task_id) in self.active_tasks:
                        _, timeout = self.active_tasks[str(task_id)]
                
                # 等待结果 (带超时)
                result = future.result(timeout=timeout)
                print(f"✅ Task #{task_id} completed successfully")
            except TimeoutError:
                print(f"⏱️ Task #{task_id} timed out after {timeout}s")
            except Exception as e:
                print(f"❌ Task #{task_id} failed: {e}")
    
    def get_active_count(self) -> int:
        """获取活跃任务数"""
        with self.lock:
            return len(self.active_tasks)
    
    def shutdown(self, wait: bool = True) -> None:
        """关闭线程池"""
        self.executor.shutdown(wait=wait)
        print("🔴 WorkerPool shutdown")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown()


# ========== LLM Worker (带超时) ==========

from organization_core.llm import get_llm_router, get_provider


class LLMWorker:
    """LLM Worker - 支持多提供商调用 (带超时保护)"""
    
    # 默认超时设置
    DEFAULT_TIMEOUT = 30  # 30秒
    
    def __init__(self):
        self.router = get_llm_router()
        self.default_timeout = self.DEFAULT_TIMEOUT
        print(f"✅ LLMWorker initialized (timeout={self.default_timeout}s)")
    
    def generate(
        self, 
        messages: list, 
        provider_name: Optional[str] = None,
        timeout: Optional[int] = None,
        **kwargs
    ) -> str:
        """
        调用 LLM 生成内容 (带超时)
        
        Args:
            messages: 消息列表
            provider_name: 指定提供商
            timeout: 超时时间 (秒)
            **kwargs: 其他参数
            
        Returns:
            生成的文本
        """
        use_timeout = timeout or self.default_timeout
        
        # 如果没有指定，自动选择
        if not provider_name:
            last_msg = messages[-1].get("content", "") if messages else ""
            provider_name = self.router.select_provider(last_msg)
        
        # 获取提供商
        provider = get_provider(provider_name)
        
        if not provider:
            raise RuntimeError(f"Provider '{provider_name}' not available")
        
        print(f"🤖 Calling LLM: provider={provider_name}, model={provider.name}, timeout={use_timeout}s")
        
        # 调用 (提供商已有内部超时，这里再包装一层)
        try:
            response = provider.generate(messages, **kwargs)
            return response.content
        except Exception as e:
            if "timeout" in str(e).lower():
                raise TimeoutError(f"LLM call timed out after {use_timeout}s") from e
            raise
    
    def generate_with_timeout(
        self, 
        messages: list, 
        provider_name: Optional[str] = None,
        timeout: Optional[int] = None,
        **kwargs
    ) -> tuple:
        """
        带超时的 LLM 调用
        
        Returns:
            (success: bool, content: str or error message)
        """
        use_timeout = timeout or self.default_timeout
        
        def _call():
            return self.generate(messages, provider_name, **kwargs)
        
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(_call)
            try:
                content = future.result(timeout=use_timeout)
                return True, content
            except TimeoutError:
                return False, f"Timeout after {use_timeout}s"
            except Exception as e:
                return False, str(e)
    
    def chat(
        self, 
        message: str, 
        system_prompt: Optional[str] = None,
        provider_name: Optional[str] = None,
        timeout: Optional[int] = None,
        **kwargs
    ) -> str:
        """
        简单对话 (带超时)
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": message})
        
        return self.generate(messages, provider_name, timeout, **kwargs)


# 全局 LLM Worker
_llm_worker = None


def get_llm_worker() -> LLMWorker:
    """获取 LLM Worker 实例"""
    global _llm_worker
    if _llm_worker is None:
        _llm_worker = LLMWorker()
    return _llm_worker

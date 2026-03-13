#!/usr/bin/env python3
"""
Autonomous Runner - 自主运行系统
自动处理任务、自动协作、自动优化
"""
import time
from datetime import datetime
from typing import Dict, List, Callable


class TaskQueue:
    """任务队列"""
    
    def __init__(self):
        self.queue = []
        self.priority_queue = []
    
    def add(self, task: Dict, priority: int = 0):
        """添加任务"""
        task["added_at"] = datetime.now().isoformat()
        
        if priority > 0:
            self.priority_queue.append(task)
        else:
            self.queue.append(task)
    
    def get(self) -> Dict:
        """获取任务"""
        # 优先队列优先
        if self.priority_queue:
            return self.priority_queue.pop(0)
        if self.queue:
            return self.queue.pop(0)
        return None
    
    def size(self) -> int:
        return len(self.queue) + len(self.priority_queue)
    
    def clear(self):
        self.queue.clear()
        self.priority_queue.clear()


class AutonomousRunner:
    """自主运行系统"""
    
    def __init__(self):
        self.task_queue = TaskQueue()
        self.running = False
        self.executor = None
        self.handlers = {}
        self.stats = {
            "total_tasks": 0,
            "completed": 0,
            "failed": 0,
        }
        self.autonomous_mode = True  # 自动模式
    
    def set_executor(self, executor):
        """设置执行器"""
        self.executor = executor
    
    def register_handler(self, event_type: str, handler: Callable):
        """注册事件处理器"""
        self.handlers[event_type] = handler
    
    def add_task(self, task: Dict, priority: int = 0):
        """添加任务"""
        self.task_queue.add(task, priority)
        print(f"📝 添加任务: {task.get('goal', task.get('description', 'unknown'))}")
    
    def add_simple_task(self, description: str, priority: int = 0):
        """添加简单任务"""
        task = {
            "goal": description,
            "subtasks": [],
            "priority": priority,
        }
        self.add_task(task, priority)
    
    def execute_task(self, task: Dict) -> Dict:
        """执行任务"""
        self.stats["total_tasks"] += 1
        
        if self.executor:
            try:
                result = self.executor.execute(task)
                self.stats["completed"] += 1
                return result
            except Exception as e:
                self.stats["failed"] += 1
                return {"error": str(e)}
        else:
            # 简单执行
            print(f"   执行: {task.get('goal', 'unknown')}")
            self.stats["completed"] += 1
            return {"status": "completed"}
    
    def run(self):
        """运行主循环"""
        self.running = True
        
        print("🚀 自主运行系统启动")
        print(f"   自动模式: {'开启' if self.autonomous_mode else '关闭'}")
        print("="*50)
        
        while self.running:
            # 获取任务
            task = self.task_queue.get()
            
            if task:
                print(f"\n📋 处理任务: {task.get('goal', 'unknown')}")
                
                # 执行
                result = self.execute_task(task)
                
                # 触发完成事件
                if "task_completed" in self.handlers:
                    self.handlers["task_completed"](task, result)
                
                print(f"   ✅ 完成")
            
            else:
                # 空闲时执行自动任务
                if self.autonomous_mode:
                    self._run_autonomous_tasks()
            
            # 等待
            time.sleep(1)
        
        print("\n🛑 自主运行系统停止")
    
    def _run_autonomous_tasks(self):
        """执行自动任务"""
        # 可以添加定期任务、健康检查等
        pass
    
    def stop(self):
        """停止"""
        self.running = False
    
    def get_status(self) -> Dict:
        """获取状态"""
        return {
            "running": self.running,
            "queue_size": self.task_queue.size(),
            "stats": self.stats.copy(),
            "autonomous_mode": self.autonomous_mode,
        }
    
    def print_status(self):
        """打印状态"""
        status = self.get_status()
        
        print("="*50)
        print("      Autonomous Runner 状态")
        print("="*50)
        print(f"运行中: {'是' if status['running'] else '否'}")
        print(f"队列任务: {status['queue_size']}")
        print(f"已完成: {status['stats']['completed']}")
        print(f"失败: {status['stats']['failed']}")
        print(f"自动模式: {'开启' if status['autonomous_mode'] else '关闭'}")
        print("="*50)
    
    def enable_autonomous(self):
        """启用自动模式"""
        self.autonomous_mode = True
        print("✅ 自动模式已启用")
    
    def disable_autonomous(self):
        """禁用自动模式"""
        self.autonomous_mode = False
        print("⚠️ 自动模式已禁用")


# 测试
if __name__ == "__main__":
    print("=== Autonomous Runner 测试 ===\n")
    
    # 创建
    runner = AutonomousRunner()
    
    # 添加任务
    runner.add_simple_task("写一个Python函数")
    runner.add_simple_task("分析数据")
    runner.add_simple_task("写一个爬虫", priority=1)  # 高优先级
    
    # 状态
    runner.print_status()
    
    # 模拟执行一轮
    print("\n模拟执行:")
    task = runner.task_queue.get()
    if task:
        print(f"执行: {task.get('goal')}")
    
    runner.print_status()

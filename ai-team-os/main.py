#!/usr/bin/env python3
"""
AI Team OS - 主入口
整合所有系统
"""
import sys
import os

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))

from task_system.task_executor import TaskExecutor
from memory.ai_memory import AIMemory
from memory.experience_log import ExperienceLog
from runtime.autonomous_runner import AutonomousRunner


class AITeamOS:
    """AI Team OS - 整合所有系统"""
    
    def __init__(self):
        self.executor = TaskExecutor()
        self.memory = AIMemory()
        self.experience = ExperienceLog()
        self.runner = AutonomousRunner()
        
        # 注册Agent
        self._register_agents()
    
    def _register_agents(self):
        """注册Agent"""
        # 简单Agent注册
        pass
    
    def execute(self, task: str) -> dict:
        """执行任务"""
        print(f"\n{'='*50}")
        print(f"🎯 任务: {task}")
        print(f"{'='*50}")
        
        # 1. 查记忆
        recall = self.memory.recall(task)
        
        if recall.get("solution"):
            print(f"💡 找到相似方案: {recall['solution']['task']}")
        
        # 2. 执行
        result = self.executor.execute({"goal": task})
        
        # 3. 记录经验
        if result.get("status") == "completed":
            self.experience.log_success(task, "executor", "mixed", "success")
            self.memory.save_solution(task, str(result))
        
        return result
    
    def add_task(self, task: str):
        """添加任务到队列"""
        self.runner.add_simple_task(task)
    
    def run(self):
        """启动自动运行"""
        self.runner.run()
    
    def stop(self):
        """停止"""
        self.runner.stop()


# 全局实例
_os = None

def get_ai_team_os() -> AITeamOS:
    global _os
    if _os is None:
        _os = AITeamOS()
    return _os


# 便捷函数
def execute(task: str):
    """执行任务"""
    return get_ai_team_os().execute(task)


# 测试
if __name__ == "__main__":
    os = get_ai_team_os()
    
    print("=== AI Team OS 测试 ===\n")
    
    # 执行任务
    result = os.execute("写一个Python爬虫")
    
    print(f"\n结果: {result.get('summary', '完成')}")

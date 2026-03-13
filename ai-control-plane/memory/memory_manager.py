#!/usr/bin/env python3
"""
Memory Manager - 记忆管理器
统一管理所有记忆系统
"""
from ai_memory import AIMemory
from experience_log import ExperienceLog
from vector_memory import VectorMemory


class MemoryManager:
    """记忆管理器"""
    
    def __init__(self):
        self.ai_memory = AIMemory()
        self.experience = ExperienceLog()
        self.vector = VectorMemory()
    
    # ===== AI Memory =====
    
    def remember_solution(self, task: str, solution: str, tags: list = None):
        """记忆成功方案"""
        self.ai_memory.save_solution(task, solution, tags)
    
    def remember_error(self, task: str, error: str, solution: str = None):
        """记忆错误案例"""
        self.ai_memory.save_error(task, error, solution)
    
    def recall(self, keyword: str):
        """回忆"""
        return self.ai_memory.recall(keyword)
    
    # ===== Experience =====
    
    def log_task(self, task: str, agent: str, model: str, result: str, success: bool):
        """记录任务"""
        self.experience.log_task(task, agent, model, result, success)
    
    def get_stats(self) -> dict:
        """获取统计"""
        return {
            "memory": self.ai_memory.get_stats(),
            "experience": self.experience.get_stats(),
        }
    
    def print_status(self):
        """打印状态"""
        stats = self.get_stats()
        
        print("="*50)
        print("      Memory Manager")
        print("="*50)
        
        m = stats["memory"]
        print(f"✅ 成功方案: {m['success_solutions']}")
        print(f"❌ 错误案例: {m['error_cases']}")
        print(f"📈 优化策略: {m['optimization_strategies']}")
        print(f"📚 知识点: {m['knowledge']}")
        
        e = stats["experience"]
        print(f"\n📊 经验统计:")
        print(f"   总数: {e['total']}")
        print(f"   成功率: {e['success_rate']:.1f}%")
        
        print("="*50)


# 全局实例
_manager = None

def get_memory_manager() -> MemoryManager:
    global _manager
    if _manager is None:
        _manager = MemoryManager()
    return _manager


# 测试
if __name__ == "__main__":
    mgr = get_memory_manager()
    
    print("=== Memory Manager 测试 ===\n")
    
    # 记忆
    mgr.remember_solution("Python爬虫", "使用requests+bs4")
    mgr.remember_error("爬虫被封", "使用代理池解决")
    
    # 记录任务
    mgr.log_task("写爬虫", "Coder", "deepseek-coder", "完成", True)
    mgr.log_task("分析数据", "Analyst", "qwen2.5:14b", "完成", True)
    
    # 状态
    mgr.print_status()

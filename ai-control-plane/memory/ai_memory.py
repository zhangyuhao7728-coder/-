#!/usr/bin/env python3
"""
AI Memory System - AI记忆系统
记录成功方案、错误案例、优化策略
"""
import json
from datetime import datetime
from typing import Dict, List, Optional


class AIMemory:
    """AI记忆系统"""
    
    def __init__(self):
        self.success_solutions = []  # 成功方案
        self.error_cases = []        # 错误案例
        self.optimization_strategies = []  # 优化策略
        self.key_words = []          # 关键知识点
    
    # ========== 成功方案 ==========
    
    def save_solution(self, task: str, solution: str, tags: List[str] = None):
        """保存成功方案"""
        memory = {
            "task": task,
            "solution": solution,
            "tags": tags or [],
            "timestamp": datetime.now().isoformat(),
            "usage_count": 0,
        }
        self.success_solutions.append(memory)
        print(f"✅ 保存成功方案: {task[:30]}")
    
    def find_solution(self, keyword: str) -> Optional[Dict]:
        """查找成功方案"""
        for m in reversed(self.success_solutions):
            if keyword in m["task"] or keyword in m.get("tags", []):
                m["usage_count"] = m.get("usage_count", 0) + 1
                return m
        return None
    
    def get_popular_solutions(self, n: int = 5) -> List[Dict]:
        """获取热门方案"""
        sorted_list = sorted(
            self.success_solutions, 
            key=lambda x: x.get("usage_count", 0), 
            reverse=True
        )
        return sorted_list[:n]
    
    # ========== 错误案例 ==========
    
    def save_error(self, task: str, error: str, solution: str = None):
        """保存错误案例"""
        memory = {
            "task": task,
            "error": error,
            "solution": solution,
            "timestamp": datetime.now().isoformat(),
        }
        self.error_cases.append(memory)
        print(f"❌ 保存错误案例: {task[:30]}")
    
    def find_error(self, keyword: str) -> Optional[Dict]:
        """查找错误案例"""
        for m in reversed(self.error_cases):
            if keyword in m["task"] or keyword in m.get("error", ""):
                return m
        return None
    
    # ========== 优化策略 ==========
    
    def save_strategy(self, name: str, description: str, scenario: str):
        """保存优化策略"""
        strategy = {
            "name": name,
            "description": description,
            "scenario": scenario,
            "timestamp": datetime.now().isoformat(),
        }
        self.optimization_strategies.append(strategy)
        print(f"📈 保存优化策略: {name}")
    
    def find_strategy(self, scenario: str) -> Optional[Dict]:
        """查找优化策略"""
        for m in reversed(self.optimization_strategies):
            if scenario in m.get("scenario", ""):
                return m
        return None
    
    # ========== 关键知识点 ==========
    
    def save_knowledge(self, keyword: str, content: str):
        """保存关键知识点"""
        knowledge = {
            "keyword": keyword,
            "content": content,
            "timestamp": datetime.now().isoformat(),
        }
        self.key_words.append(knowledge)
        print(f"📚 保存知识点: {keyword}")
    
    def find_knowledge(self, keyword: str) -> Optional[Dict]:
        """查找知识点"""
        for m in reversed(self.key_words):
            if keyword in m.get("keyword", ""):
                return m
        return None
    
    # ========== 记忆复用 ==========
    
    def recall(self, task: str) -> Dict:
        """回忆相关记忆"""
        result = {
            "solution": self.find_solution(task),
            "error": self.find_error(task),
            "strategy": self.find_strategy(task),
            "knowledge": self.find_knowledge(task),
        }
        return result
    
    # ========== 统计 ==========
    
    def get_stats(self) -> Dict:
        """获取统计"""
        return {
            "success_solutions": len(self.success_solutions),
            "error_cases": len(self.error_cases),
            "optimization_strategies": len(self.optimization_strategies),
            "knowledge": len(self.key_words),
        }
    
    def print_stats(self):
        """打印统计"""
        stats = self.get_stats()
        
        print("="*50)
        print("         AI Memory System")
        print("="*50)
        print(f"✅ 成功方案: {stats['success_solutions']}")
        print(f"❌ 错误案例: {stats['error_cases']}")
        print(f"📈 优化策略: {stats['optimization_strategies']}")
        print(f"📚 知识点: {stats['knowledge']}")
        print("="*50)
    
    # ========== 保存/加载 ==========
    
    def save(self, filepath: str = "ai_memory.json"):
        """保存记忆"""
        data = {
            "success_solutions": self.success_solutions,
            "error_cases": self.error_cases,
            "optimization_strategies": self.optimization_strategies,
            "key_words": self.key_words,
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 记忆已保存: {filepath}")
    
    def load(self, filepath: str = "ai_memory.json"):
        """加载记忆"""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            self.success_solutions = data.get("success_solutions", [])
            self.error_cases = data.get("error_cases", [])
            self.optimization_strategies = data.get("optimization_strategies", [])
            self.key_words = data.get("key_words", [])
            
            print(f"📂 记忆已加载: {filepath}")
        except:
            print(f"⚠️ 无法加载记忆文件")


# 全局实例
_memory = None

def get_ai_memory() -> AIMemory:
    global _memory
    if _memory is None:
        _memory = AIMemory()
    return _memory


# 便捷函数
def remember_solution(task: str, solution: str):
    """记忆成功方案"""
    get_ai_memory().save_solution(task, solution)

def recall(task: str) -> Dict:
    """回忆"""
    return get_ai_memory().recall(task)


# 测试
if __name__ == "__main__":
    memory = get_ai_memory()
    
    print("=== AI Memory System 测试 ===\n")
    
    # 保存成功方案
    memory.save_solution(
        "Python爬虫", 
        "使用requests+BeautifulSoup",
        tags=["爬虫", "Python"]
    )
    
    # 保存错误案例
    memory.save_error(
        "Python爬虫",
        "反爬虫机制",
        "使用代理池"
    )
    
    # 保存优化策略
    memory.save_strategy(
        "性能优化",
        "使用异步",
        "大数据量"
    )
    
    # 保存知识点
    memory.save_knowledge(
        "Python",
        "一种高级编程语言"
    )
    
    # 统计
    memory.print_stats()
    
    # 回忆
    print("\n回忆 '爬虫':")
    result = memory.recall("爬虫")
    if result["solution"]:
        print(f"  ✅ {result['solution']['solution']}")

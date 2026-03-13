#!/usr/bin/env python3
"""
Auto Learning System - 自动学习系统
记录成功/失败，自动优化
"""
from datetime import datetime
from typing import Dict, List


class AutoLearner:
    """自动学习系统"""
    
    def __init__(self):
        self.success_tasks = []   # 成功任务
        self.failed_tasks = []    # 失败任务
        self.optimizations = []  # 优化方法
        self.learnings = []      # 学习记录
    
    # ===== 记录 =====
    
    def record_success(self, task: str, solution: str, agent: str):
        """记录成功"""
        record = {
            "timestamp": datetime.now().isoformat(),
            "task": task,
            "solution": solution,
            "agent": agent,
            "type": "success"
        }
        self.success_tasks.append(record)
        self.learnings.append(record)
        print(f"✅ 记录成功: {task[:30]}")
    
    def record_failure(self, task: str, error: str, agent: str):
        """记录失败"""
        record = {
            "timestamp": datetime.now().isoformat(),
            "task": task,
            "error": error,
            "agent": agent,
            "type": "failure"
        }
        self.failed_tasks.append(record)
        self.learnings.append(record)
        print(f"❌ 记录失败: {task[:30]}")
    
    def record_optimization(self, method: str, scenario: str, result: str):
        """记录优化方法"""
        record = {
            "timestamp": datetime.now().isoformat(),
            "method": method,
            "scenario": scenario,
            "result": result,
            "type": "optimization"
        }
        self.optimizations.append(record)
        self.learnings.append(record)
        print(f"📈 记录优化: {method}")
    
    # ===== 自动优化 =====
    
    def analyze_failures(self) -> Dict:
        """分析失败模式"""
        if not self.failed_tasks:
            return {"pattern": "无失败记录", "suggestion": "继续努力"}
        
        # 简单分析
        errors = {}
        for f in self.failed_tasks:
            err = f.get("error", "unknown")
            errors[err] = errors.get(err, 0) + 1
        
        # 找出最常见错误
        common_error = max(errors.items(), key=lambda x: x[1])
        
        return {
            "total_failures": len(self.failed_tasks),
            "common_error": common_error[0],
            "count": common_error[1],
            "suggestion": self._get_suggestion(common_error[0])
        }
    
    def _get_suggestion(self, error: str) -> str:
        """获取建议"""
        if "timeout" in error.lower():
            return "建议使用更快的模型"
        elif "quota" in error.lower():
            return "建议切换到免费模型"
        elif "network" in error.lower():
            return "检查网络连接"
        else:
            return "需要人工介入"
    
    def get_best_solution(self, task_keyword: str) -> str:
        """获取最佳方案"""
        for s in reversed(self.success_tasks):
            if task_keyword in s.get("task", ""):
                return s.get("solution", "")
        return ""
    
    # ===== 自动学习 =====
    
    def learn(self, task: str, result: str, success: bool, agent: str):
        """自动学习"""
        if success:
            self.record_success(task, result, agent)
            
            # 检查是否需要优化
            if len(result) > 1000:
                self.record_optimization(
                    "使用更强模型",
                    "长任务",
                    "成功"
                )
        else:
            self.record_failure(task, result, agent)
            
            # 分析并优化
            analysis = self.analyze_failures()
            print(f"   💡 优化建议: {analysis.get('suggestion', '')}")
    
    # ===== 统计 =====
    
    def get_stats(self) -> Dict:
        return {
            "success": len(self.success_tasks),
            "failed": len(self.failed_tasks),
            "optimizations": len(self.optimizations),
            "success_rate": len(self.success_tasks) / max(1, len(self.learnings)) * 100
        }
    
    def print_stats(self):
        stats = self.get_stats()
        print("="*50)
        print("   Auto Learning Stats")
        print("="*50)
        print(f"✅ 成功: {stats['success']}")
        print(f"❌ 失败: {stats['failed']}")
        print(f"📈 优化: {stats['optimizations']}")
        print(f"📊 成功率: {stats['success_rate']:.1f}%")
        print("="*50)


# 全局实例
_learner = None

def get_auto_learner() -> AutoLearner:
    global _learner
    if _learner is None:
        _learner = AutoLearner()
    return _learner


# 测试
if __name__ == "__main__":
    learner = get_auto_learner()
    
    print("=== Auto Learning 测试 ===\n")
    
    # 记录
    learner.record_success("写爬虫", "使用requests+bs4", "Coder")
    learner.record_failure("分析大数据", "内存不足", "Analyst")
    learner.record_optimization("使用流处理", "大数据", "成功")
    
    # 学习
    learner.learn("新任务", "完成", True, "Coder")
    learner.learn("新任务2", "超时", False, "Coder")
    
    # 统计
    learner.print_stats()

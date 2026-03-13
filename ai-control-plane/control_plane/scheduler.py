#!/usr/bin/env python3
"""
Scheduler - 智能任务调度器
功能：
1. 任务复杂度分析
2. 自动模型选择
3. 成本优化
"""
from typing import Dict, Optional


class Scheduler:
    """任务调度器"""
    
    # 模型选择策略
    MODEL_STRATEGY = {
        # 复杂度 -> 模型
        "low": {
            "model": "qwen2.5:latest",
            "cost": "free",
            "speed": "fast",
        },
        "medium": {
            "model": "deepseek-coder:6.7b",
            "cost": "free",
            "speed": "medium",
        },
        "high": {
            "model": "qwen3.5:9b",
            "cost": "free",
            "speed": "slow",
        },
        # 任务类型 -> 模型
        "code": {
            "model": "deepseek-coder:6.7b",
            "cost": "free",
            "speed": "medium",
        },
        "analysis": {
            "model": "qwen3.5:9b",
            "cost": "free",
            "speed": "slow",
        },
        "creative": {
            "model": "minimax/MiniMax-M2.5",
            "cost": "paid",
            "speed": "medium",
        },
        "fast": {
            "model": "qwen2.5:latest",
            "cost": "free",
            "speed": "fast",
        },
    }
    
    def __init__(self):
        self.stats = {
            "total_tasks": 0,
            "by_complexity": {},
            "by_type": {},
            "cost_saved": 0,
        }
    
    # ========== 复杂度分析 ==========
    
    def analyze_complexity(self, prompt: str) -> str:
        """
        分析任务复杂度
        
        返回: low / medium / high
        """
        prompt_lower = prompt.lower()
        
        # 高复杂度指标
        high_complexity = [
            "分析", "比较", "评估", "设计", "架构",
            "algorithm", "analyze", "compare", "design",
            "解释原理", "详细", "全面"
        ]
        
        # 低复杂度指标
        low_complexity = [
            "简单", "快速", "一句话", "是什么",
            "hello", "hi", "简单介绍"
        ]
        
        # 检查
        if any(kw in prompt_lower for kw in high_complexity):
            return "high"
        
        if any(kw in prompt_lower for kw in low_complexity):
            return "low"
        
        return "medium"
    
    # ========== 模型选择 ==========
    
    def choose_model(self, task_type: str = None, complexity: str = None, prompt: str = None) -> Dict:
        """
        选择最佳模型
        
        Args:
            task_type: 任务类型 (code/analysis/creative/fast)
            complexity: 复杂度 (low/medium/high)
            prompt: 用户输入 (自动分析)
        
        Returns:
            {"model": "...", "cost": "...", "reason": "..."}
        """
        self.stats["total_tasks"] += 1
        
        # 自动分析
        if task_type is None and prompt:
            task_type = self._detect_task_type(prompt)
        
        if complexity is None and prompt:
            complexity = self.analyze_complexity(prompt)
        
        # 确定优先级
        # 1. 任务类型优先
        # 2. 复杂度次之
        
        selected = None
        reason = ""
        
        if task_type and task_type in self.MODEL_STRATEGY:
            selected = self.MODEL_STRATEGY[task_type]["model"]
            reason = f"任务类型: {task_type}"
            self.stats["by_type"][task_type] = self.stats["by_type"].get(task_type, 0) + 1
        
        elif complexity and complexity in self.MODEL_STRATEGY:
            selected = self.MODEL_STRATEGY[complexity]["model"]
            reason = f"复杂度: {complexity}"
            self.stats["by_complexity"][complexity] = self.stats["by_complexity"].get(complexity, 0) + 1
        
        # 默认
        if not selected:
            selected = "qwen2.5:latest"
            reason = "默认选择"
        
        # 计算节省成本
        if "minimax" not in selected:
            self.stats["cost_saved"] += 0.01  # 估算节省
        
        return {
            "model": selected,
            "task_type": task_type,
            "complexity": complexity,
            "reason": reason,
            "strategy": self.MODEL_STRATEGY.get(task_type, self.MODEL_STRATEGY.get("low")),
        }
    
    def _detect_task_type(self, prompt: str) -> str:
        """检测任务类型"""
        prompt_lower = prompt.lower()
        
        if any(kw in prompt_lower for kw in ["python", "代码", "编程", "function", "def "]):
            return "code"
        
        if any(kw in prompt_lower for kw in ["分析", "比较", "解释", "为什么"]):
            return "analysis"
        
        if any(kw in prompt_lower for kw in ["创作", "写诗", "故事", "小说"]):
            return "creative"
        
        if any(kw in prompt_lower for kw in ["简单", "快速", "一句话", "是什么"]):
            return "fast"
        
        return "general"
    
    # ========== 调度 ==========
    
    def schedule(self, prompt: str) -> Dict:
        """
        完整调度
        
        1. 分析任务
        2. 选择模型
        3. 返回策略
        """
        task_type = self._detect_task_type(prompt)
        complexity = self.analyze_complexity(prompt)
        
        return self.choose_model(
            task_type=task_type,
            complexity=complexity,
            prompt=prompt
        )
    
    def get_stats(self) -> Dict:
        return self.stats.copy()


# 全局实例
_scheduler = None

def get_scheduler() -> Scheduler:
    global _scheduler
    if _scheduler is None:
        _scheduler = Scheduler()
    return _scheduler


def choose_model(task_type: str = None, complexity: str = None, prompt: str = None) -> Dict:
    """选择模型"""
    return get_scheduler().choose_model(task_type, complexity, prompt)


# 测试
if __name__ == "__main__":
    sch = get_scheduler()
    
    print("=== Scheduler 测试 ===\n")
    
    tests = [
        "帮我写一个Python函数",
        "分析这段代码的复杂度",
        "写一首诗",
        "什么是AI？",
        "帮我设计一个系统架构",
    ]
    
    for prompt in tests:
        result = sch.schedule(prompt)
        
        print(f"输入: {prompt}")
        print(f"  → 任务: {result['task_type']}, 复杂度: {result['complexity']}")
        print(f"  → 模型: {result['model']}")
        print(f"  → 原因: {result['reason']}")
        print()
    
    print(f"统计: {sch.get_stats()}")

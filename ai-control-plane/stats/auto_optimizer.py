#!/usr/bin/env python3
"""
Auto Optimizer - 自动策略优化
功能：
1. 收集模型表现数据
2. 计算模型评分
3. 自动调整优先级
"""
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List


class AutoOptimizer:
    """自动优化器"""
    
    CONFIG_DIR = os.path.expanduser("~/项目/Ai学习系统/ai-control-plane/stats")
    
    def __init__(self):
        os.makedirs(self.CONFIG_DIR, exist_ok=True)
        
        # 模型评分文件
        self.model_scores_file = os.path.join(self.CONFIG_DIR, "model_scores.json")
        self.model_scores = self._load_scores()
        
        # 基础评分
        self.base_scores = {
            "qwen2.5:latest": 0.7,
            "qwen2.5:7b": 0.75,
            "qwen3.5:9b": 0.8,
            "deepseek-coder:6.7b": 0.8,
            "minimax/MiniMax-M2.5": 0.9,
            "volcengine/doubao-seed-code": 0.85,
        }
        
        # 权重
        self.weights = {
            "success_rate": 0.4,    # 成功率权重
            "speed": 0.3,          # 速度权重
            "quality": 0.3,        # 质量权重
        }
    
    def _load_scores(self) -> Dict:
        """加载评分"""
        if os.path.exists(self.model_scores_file):
            with open(self.model_scores_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_scores(self):
        """保存评分"""
        with open(self.model_scores_file, 'w') as f:
            json.dump(self.model_scores, f, indent=2)
    
    # ========== 收集数据 ==========
    
    def record_success(self, model: str):
        """记录成功"""
        if model not in self.model_scores:
            self.model_scores[model] = {
                "success": 0,
                "failed": 0,
                "total_latency": 0,
                "total_quality": 0,
                "calls": 0,
            }
        
        self.model_scores[model]["success"] += 1
        self.model_scores[model]["calls"] += 1
        self._save_scores()
    
    def record_failure(self, model: str):
        """记录失败"""
        if model not in self.model_scores:
            self.model_scores[model] = {
                "success": 0,
                "failed": 0,
                "total_latency": 0,
                "total_quality": 0,
                "calls": 0,
            }
        
        self.model_scores[model]["failed"] += 1
        self.model_scores[model]["calls"] += 1
        self._save_scores()
    
    def record_latency(self, model: str, latency_ms: int):
        """记录延迟"""
        if model in self.model_scores:
            self.model_scores[model]["total_latency"] += latency_ms
            self._save_scores()
    
    def record_quality(self, model: str, quality: float):
        """记录质量"""
        if model in self.model_scores:
            self.model_scores[model]["total_quality"] += quality
            self._save_scores()
    
    # ========== 计算评分 ==========
    
    def calculate_score(self, model: str) -> float:
        """
        计算模型评分
        
        综合考虑:
        - 成功率 (40%)
        - 速度 (30%)
        - 质量 (30%)
        """
        if model not in self.model_scores:
            # 使用基础评分
            return self.base_scores.get(model, 0.5)
        
        data = self.model_scores[model]
        calls = data.get("calls", 0)
        
        if calls == 0:
            return self.base_scores.get(model, 0.5)
        
        # 1. 成功率
        success = data.get("success", 0)
        success_rate = success / calls
        
        # 2. 速度 (延迟越低越好)
        avg_latency = data.get("total_latency", 0) / calls
        speed_score = max(0, 1 - (avg_latency / 10000))  # 假设10秒为最慢
        
        # 3. 质量
        avg_quality = data.get("total_quality", 0) / calls
        
        # 综合评分
        score = (
            success_rate * self.weights["success_rate"] +
            speed_score * self.weights["speed"] +
            avg_quality * self.weights["quality"]
        )
        
        return round(score, 3)
    
    # ========== 优化优先级 ==========
    
    def get_optimized_priority(self, models: List[str]) -> List[str]:
        """
        获取优化后的优先级
        
        评分高的模型排在前面
        """
        scored = []
        
        for model in models:
            score = self.calculate_score(model)
            scored.append((model, score))
        
        # 按评分排序 (从高到低)
        scored.sort(key=lambda x: x[1], reverse=True)
        
        return [m for m, s in scored]
    
    def adjust_chain(self, chain: List[str]) -> List[str]:
        """
        调整Fallback链
        
        根据评分自动调整顺序
        """
        return self.get_optimized_priority(chain)
    
    # ========== 报告 ==========
    
    def print_scores(self):
        """打印评分"""
        print("=== Model Scores ===\n")
        
        # 合并基础评分和数据
        all_models = set(self.base_scores.keys()) | set(self.model_scores.keys())
        
        scored = []
        for model in all_models:
            score = self.calculate_score(model)
            data = self.model_scores.get(model, {})
            calls = data.get("calls", 0)
            
            scored.append((model, score, calls))
        
        # 按评分排序
        scored.sort(key=lambda x: x[1], reverse=True)
        
        for model, score, calls in scored:
            base = "⭐" if score >= 0.8 else "📊"
            print(f"{base} {model}: {score:.3f} (调用: {calls})")
        
        print(f"\n权重: 成功率{self.weights['success_rate']*100:.0f}% | 速度{self.weights['speed']*100:.0f}% | 质量{self.weights['quality']*100:.0f}%")
    
    def recommend_chain(self, task_type: str = None) -> List[str]:
        """推荐最优链"""
        # 默认链
        default = [
            "minimax/MiniMax-M2.5",
            "volcengine/doubao-seed-code",
            "qwen3.5:9b",
            "deepseek-coder:6.7b",
            "qwen2.5:latest",
        ]
        
        return self.adjust_chain(default)


# 全局实例
_optimizer = None

def get_auto_optimizer() -> AutoOptimizer:
    global _optimizer
    if _optimizer is None:
        _optimizer = AutoOptimizer()
    return _optimizer


# 测试
if __name__ == "__main__":
    opt = get_auto_optimizer()
    
    print("=== Auto Optimizer 测试 ===\n")
    
    # 模拟记录
    opt.record_success("qwen3.5:9b")
    opt.record_success("qwen3.5:9b")
    opt.record_failure("qwen3.5:9b")
    
    opt.record_success("minimax/MiniMax-M2.5")
    opt.record_success("minimax/MiniMax-M2.5")
    opt.record_success("minimax/MiniMax-M2.5")
    
    # 打印评分
    opt.print_scores()
    
    # 推荐链
    print("\n推荐链:")
    chain = opt.recommend_chain()
    for i, m in enumerate(chain, 1):
        print(f"  {i}. {m}")

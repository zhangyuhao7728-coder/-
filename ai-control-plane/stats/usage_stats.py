#!/usr/bin/env python3
"""
Usage Stats - 使用统计
功能：
1. 调用次数统计
2. Token消耗统计
3. 费用统计
4. 成功率统计
"""
import json
import os
from datetime import datetime
from typing import Dict


class UsageStats:
    """使用统计"""
    
    STATS_DIR = os.path.expanduser("~/项目/Ai学习系统/ai-control-plane/stats")
    
    def __init__(self):
        # 确保目录存在
        os.makedirs(self.STATS_DIR, exist_ok=True)
        
        # 文件路径
        self.usage_file = os.path.join(self.STATS_DIR, "usage.json")
        self.cost_file = os.path.join(self.STATS_DIR, "cost.json")
        self.model_file = os.path.join(self.STATS_DIR, "model_usage.json")
        
        # 加载数据
        self.usage = self._load_json(self.usage_file)
        self.cost = self._load_json(self.cost_file)
        self.model_usage = self._load_json(self.model_file)
    
    def _load_json(self, filepath: str) -> Dict:
        """加载JSON"""
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_json(self, filepath: str, data: Dict):
        """保存JSON"""
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    # ========== 记录调用 ==========
    
    def record_call(self, model: str, tokens: int = 0, cost: float = 0, success: bool = True):
        """记录一次调用"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        # 1. 基础使用统计
        if today not in self.usage:
            self.usage[today] = {"calls": 0, "tokens": 0, "success": 0, "failed": 0}
        
        self.usage[today]["calls"] += 1
        self.usage[today]["tokens"] += tokens
        
        if success:
            self.usage[today]["success"] += 1
        else:
            self.usage[today]["failed"] += 1
        
        # 2. 费用统计
        if today not in self.cost:
            self.cost[today] = 0.0
        
        self.cost[today] += cost
        
        # 3. 模型使用统计
        if model not in self.model_usage:
            self.model_usage[model] = {
                "calls": 0,
                "tokens": 0,
                "cost": 0.0,
                "success": 0,
                "failed": 0,
            }
        
        self.model_usage[model]["calls"] += 1
        self.model_usage[model]["tokens"] += tokens
        self.model_usage[model]["cost"] += cost
        
        if success:
            self.model_usage[model]["success"] += 1
        else:
            self.model_usage[model]["failed"] += 1
        
        # 保存
        self._save_json(self.usage_file, self.usage)
        self._save_json(self.cost_file, self.cost)
        self._save_json(self.model_file, self.model_usage)
    
    # ========== 查询 ==========
    
    def get_today_stats(self) -> Dict:
        """获取今日统计"""
        today = datetime.now().strftime("%Y-%m-%d")
        return self.usage.get(today, {"calls": 0, "tokens": 0, "success": 0, "failed": 0})
    
    def get_model_stats(self, model: str = None) -> Dict:
        """获取模型统计"""
        if model:
            return self.model_usage.get(model, {})
        return self.model_usage
    
    def get_success_rate(self, model: str = None) -> float:
        """获取成功率"""
        if model:
            stats = self.model_usage.get(model, {})
            calls = stats.get("calls", 0)
            success = stats.get("success", 0)
            return (success / calls * 100) if calls > 0 else 0
        
        # 全部
        total_calls = sum(s.get("calls", 0) for s in self.usage.values())
        total_success = sum(s.get("success", 0) for s in self.usage.values())
        return (total_success / total_calls * 100) if total_calls > 0 else 0
    
    # ========== 报告 ==========
    
    def print_report(self):
        """打印报告"""
        today = self.get_today_stats()
        total_cost = sum(self.cost.values())
        
        print("=== 使用统计 ===\n")
        
        print(f"今日:")
        print(f"  调用次数: {today.get('calls', 0)}")
        print(f"  Token消耗: {today.get('tokens', 0):,}")
        print(f"  成功: {today.get('success', 0)}")
        print(f"  失败: {today.get('failed', 0)}")
        
        if today.get('calls', 0) > 0:
            rate = today['success'] / today['calls'] * 100
            print(f"  成功率: {rate:.1f}%")
        
        print(f"\n总费用: {total_cost:.4f} 元")
        
        print(f"\n模型使用:")
        for model, stats in self.model_usage.items():
            calls = stats.get('calls', 0)
            success = stats.get('success', 0)
            rate = (success / calls * 100) if calls > 0 else 0
            print(f"  {model}: {calls}次 ({rate:.1f}%)")


# 全局实例
_stats = None

def get_usage_stats() -> UsageStats:
    global _stats
    if _stats is None:
        _stats = UsageStats()
    return _stats


def record_call(model: str, tokens: int = 0, cost: float = 0, success: bool = True):
    """记录调用"""
    get_usage_stats().record_call(model, tokens, cost, success)


# 测试
if __name__ == "__main__":
    stats = get_usage_stats()
    
    print("=== Usage Stats 测试 ===\n")
    
    # 模拟记录
    record_call("minimax/MiniMax-M2.5", 1000, 0.01, True)
    record_call("qwen2.5:latest", 500, 0, True)
    record_call("qwen3.5:9b", 800, 0, False)
    
    # 报告
    stats.print_report()

#!/usr/bin/env python3
"""
Cost Monitor - 成本监控
功能：
1. 模型费用统计
2. 每日费用追踪
3. 预算告警
"""
from typing import Dict
from datetime import datetime, timedelta


class CostMonitor:
    """成本监控器"""
    
    # 模型费用 (每1K tokens)
    MODEL_COST = {
        "minimax/MiniMax-M2.5": 0.002,
        "volcengine/doubao-seed-code": 0.001,
        "qwen2.5:latest": 0,          # 免费
        "qwen2.5:7b": 0,             # 免费
        "qwen3.5:9b": 0,             # 免费
        "deepseek-coder:6.7b": 0,    # 免费
    }
    
    # 每日预算
    DAILY_BUDGET = 10.0  # 10元/天
    
    def __init__(self):
        # 费用统计
        self.total_cost = 0.0
        self.model_costs = {}  # 每个模型的费用
        self.daily_costs = {}  # 每日费用
        
        # Token统计
        self.total_tokens = 0
        self.model_tokens = {}
        
        # 历史记录
        self.history = []
        
        # 最后重置日期
        self.last_reset = datetime.now().date()
    
    def _get_date_key(self) -> str:
        """获取日期键"""
        return datetime.now().strftime("%Y-%m-%d")
    
    def update_cost(self, model: str, tokens: int):
        """
        更新费用
        
        Args:
            model: 模型名称
            tokens: 消耗的tokens
        """
        # 计算费用
        cost_per_1k = self.MODEL_COST.get(model, 0)
        cost = (tokens / 1000) * cost_per_1k
        
        # 更新统计
        self.total_cost += cost
        self.model_costs[model] = self.model_costs.get(model, 0) + cost
        
        self.total_tokens += tokens
        self.model_tokens[model] = self.model_tokens.get(model, 0) + tokens
        
        # 更新每日费用
        date_key = self._get_date_key()
        self.daily_costs[date_key] = self.daily_costs.get(date_key, 0) + cost
        
        # 记录历史
        self.history.append({
            "model": model,
            "tokens": tokens,
            "cost": cost,
            "time": datetime.now().isoformat(),
            "date": date_key,
        })
        
        # 保留最近1000条
        self.history = self.history[-1000:]
        
        return cost
    
    def get_model_cost(self, model: str) -> float:
        """获取模型费用"""
        return self.model_costs.get(model, 0)
    
    def get_daily_cost(self, date: str = None) -> float:
        """获取每日费用"""
        if date is None:
            date = self._get_date_key()
        return self.daily_costs.get(date, 0)
    
    def get_total_cost(self) -> float:
        """获取总费用"""
        return self.total_cost
    
    def get_remaining_budget(self) -> float:
        """获取剩余预算"""
        daily = self.get_daily_cost()
        return max(0, self.DAILY_BUDGET - daily)
    
    def should_alert(self) -> tuple:
        """是否应该告警"""
        daily = self.get_daily_cost()
        pct = (daily / self.DAILY_BUDGET) * 100
        
        if pct >= 100:
            return True, "critical", f"超出预算! {daily:.2f}元"
        elif pct >= 80:
            return True, "warning", f"接近预算 {pct:.0f}%"
        elif pct >= 50:
            return True, "info", f"已使用 {pct:.0f}%"
        
        return False, "", ""
    
    def reset_daily(self):
        """重置每日统计"""
        today = datetime.now().date()
        
        if today > self.last_reset:
            # 新的一天，重置
            self.daily_costs = {self._get_date_key(): 0}
            self.last_reset = today
    
    def get_stats(self) -> Dict:
        """获取统计"""
        alert, level, msg = self.should_alert()
        
        return {
            "total_cost": round(self.total_cost, 4),
            "total_tokens": self.total_tokens,
            "daily_cost": round(self.get_daily_cost(), 4),
            "daily_budget": self.DAILY_BUDGET,
            "remaining": round(self.get_remaining_budget(), 4),
            "alert": alert,
            "alert_level": level,
            "alert_message": msg,
            "model_costs": {k: round(v, 4) for k, v in self.model_costs.items()},
            "model_tokens": self.model_tokens,
        }
    
    def print_daily_report(self):
        """打印每日报告"""
        stats = self.get_stats()
        
        print("=== 每日费用报告 ===\n")
        print(f"今日费用: {stats['daily_cost']:.4f} 元")
        print(f"预算: {stats['daily_budget']} 元")
        print(f"剩余: {stats['remaining']:.4f} 元")
        
        if stats['alert']:
            print(f"\n⚠️ {stats['alert_message']}")
        
        # 模型费用
        print("\n模型费用:")
        for model, cost in stats['model_costs'].items():
            tokens = stats['model_tokens'].get(model, 0)
            print(f"  {model}: {cost:.4f}元 ({tokens} tokens)")
    
    def print_summary(self):
        """打印摘要"""
        stats = self.get_stats()
        
        print("=== 成本摘要 ===\n")
        print(f"总费用: {stats['total_cost']:.4f} 元")
        print(f"总Tokens: {stats['total_tokens']:,}")
        print(f"今日: {stats['daily_cost']:.4f} 元")


# 全局实例
_monitor = None

def get_cost_monitor() -> CostMonitor:
    global _monitor
    if _monitor is None:
        _monitor = CostMonitor()
    return _monitor


def update_cost(model: str, tokens: int):
    """更新费用"""
    return get_cost_monitor().update_cost(model, tokens)


# 测试
if __name__ == "__main__":
    monitor = get_cost_monitor()
    
    print("=== Cost Monitor 测试 ===\n")
    
    # 模拟使用
    update_cost("minimax/MiniMax-M2.5", 5000)   # 0.01元
    update_cost("minimax/MiniMax-M2.5", 3000)   # 0.006元
    update_cost("qwen2.5:latest", 1000)         # 0元
    
    # 报告
    monitor.print_daily_report()
    print()
    monitor.print_summary()

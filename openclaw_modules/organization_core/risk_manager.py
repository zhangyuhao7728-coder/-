"""
Risk Manager
风险管理系统 - 预算守护 + 风险分级
"""

from enum import Enum
from datetime import datetime, timedelta
from typing import Dict, Optional


class RiskLevel(Enum):
    """风险等级"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class RiskManager:
    """风险管理器"""
    
    # 默认预算配置
    DEFAULT_BUDGET = {
        "ceo": 100.0,
        "planner": 50.0,
        "researcher": 30.0,
        "engineer": 50.0,
        "reviewer": 20.0,
        "analyst": 30.0
    }
    
    def __init__(self, event_bus=None):
        self.event_bus = event_bus
        self.budgets = self.DEFAULT_BUDGET.copy()
        self.risk_history = []
        self.override_counts = {}  # {agent: {date: count}}
        self.costs = {}  # {agent: {date: cost}}
    
    def set_budget(self, agent: str, budget: float) -> None:
        """设置 Agent 预算"""
        self.budgets[agent] = budget
    
    def get_budget(self, agent: str) -> float:
        """获取 Agent 预算"""
        return self.budgets.get(agent, 50.0)
    
    def record_override(self, agent: str) -> None:
        """记录 Override 操作"""
        today = datetime.utcnow().strftime("%Y-%m-%d")
        
        if agent not in self.override_counts:
            self.override_counts[agent] = {}
        
        if today not in self.override_counts[agent]:
            self.override_counts[agent][today] = 0
        
        self.override_counts[agent][today] += 1
    
    def record_cost(self, agent: str, cost: float) -> None:
        """记录成本"""
        today = datetime.utcnow().strftime("%Y-%m-%d")
        
        if agent not in self.costs:
            self.costs[agent] = {}
        
        if today not in self.costs[agent]:
            self.costs[agent][today] = 0.0
        
        self.costs[agent][today] += cost
    
    def get_today_cost(self, agent: str) -> float:
        """获取今日成本"""
        today = datetime.utcnow().strftime("%Y-%m-%d")
        return self.costs.get(agent, {}).get(today, 0.0)
    
    def get_override_count(self, agent: str) -> int:
        """获取今日 Override 次数"""
        today = datetime.utcnow().strftime("%Y-%m-%d")
        return self.override_counts.get(agent, {}).get(today, 0)
    
    def check_risk(self, agent: str) -> Optional[Dict]:
        """
        检查风险
        
        Returns:
            风险信息字典，无风险返回 None
        """
        today = datetime.utcnow().strftime("%Y-%m-%d")
        override_count = self.get_override_count(agent)
        total_cost = self.get_today_cost(agent)
        budget = self.get_budget(agent)
        
        risk = None
        
        # LOW: 1次 override
        if override_count == 1:
            risk = self._emit_risk(agent, "First override", RiskLevel.LOW)
        
        # MEDIUM: >=3次 override
        elif override_count >= 3:
            risk = self._emit_risk(agent, f"Multiple overrides ({override_count})", RiskLevel.MEDIUM)
        
        # HIGH: 超过预算 150%
        if total_cost >= budget * 1.5:
            risk = self._emit_risk(agent, f"Cost exceeds 150% budget (${total_cost:.2f}/${budget:.2f})", RiskLevel.HIGH)
        
        # CRITICAL: 超过预算 200%
        if total_cost >= budget * 2.0:
            risk = self._emit_risk(agent, f"Cost exceeds 200% budget (${total_cost:.2f}/${budget:.2f})", RiskLevel.CRITICAL)
        
        return risk
    
    def _emit_risk(self, agent: str, reason: str, level: RiskLevel) -> Dict:
        """发出风险警报"""
        risk_event = {
            "agent": agent,
            "reason": reason,
            "level": level.value,
            "timestamp": datetime.utcnow().isoformat(),
            "budget": self.get_budget(agent),
            "current_cost": self.get_today_cost(agent)
        }
        
        self.risk_history.append(risk_event)
        
        # 通过 EventBus 发布
        if self.event_bus:
            self.event_bus.publish("risk_alert", risk_event)
        
        # 打印日志
        level_symbol = {
            RiskLevel.LOW: "⚠️",
            RiskLevel.MEDIUM: "⚠️⚠️",
            RiskLevel.HIGH: "🚨",
            RiskLevel.CRITICAL: "🛑"
        }
        
        print(f"{level_symbol[level]} Risk Alert [{level.value}] - {agent}: {reason}")
        
        return risk_event
    
    def get_risk_summary(self) -> Dict:
        """获取风险摘要"""
        return {
            "total_alerts": len(self.risk_history),
            "by_level": {
                "LOW": len([r for r in self.risk_history if r["level"] == "LOW"]),
                "MEDIUM": len([r for r in self.risk_history if r["level"] == "MEDIUM"]),
                "HIGH": len([r for r in self.risk_history if r["level"] == "HIGH"]),
                "CRITICAL": len([r for r in self.risk_history if r["level"] == "CRITICAL"])
            },
            "recent": self.risk_history[-10:] if self.risk_history else []
        }
    
    def clear_history(self) -> None:
        """清除风险历史"""
        self.risk_history = []


# 全局实例
_risk_manager = None


def get_risk_manager() -> RiskManager:
    """获取 RiskManager 实例"""
    global _risk_manager
    if _risk_manager is None:
        _risk_manager = RiskManager()
    return _risk_manager

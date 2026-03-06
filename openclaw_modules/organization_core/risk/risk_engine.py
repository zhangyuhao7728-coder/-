"""
Risk Engine
风险引擎 - 核心风险评估逻辑
"""

from organization_core.risk.risk_models import RiskLevel
from organization_core.risk.risk_repository import RiskRepository
from config.budget_config import BUDGET_CONFIG


class RiskEngine:
    """风险引擎 - 动态风险评估"""
    
    def __init__(self, repo: RiskRepository, budget_config: dict = None):
        self.repo = repo
        self.budget_config = budget_config or BUDGET_CONFIG
    
    def evaluate(self, agent: str) -> RiskLevel:
        """
        评估风险等级
        
        Args:
            agent: Agent 名称
            
        Returns:
            RiskLevel 或 None
        """
        # 获取最近24小时的事件
        events = self.repo.get_recent_events(agent)
        
        # 统计 Override 次数
        override_count = sum(
            1 for e in events 
            if e["type"] == "override"
        )
        
        # 统计成本
        cost_total = sum(
            e["value"] for e in events 
            if e["type"] == "cost"
        )
        
        # 获取预算
        budget = self.budget_config.get(agent, 50.0)
        
        # 计算成本比率
        cost_ratio = cost_total / budget if budget > 0 else 0
        
        # ===== 成本风险评估 (最高优先级) =====
        if cost_ratio >= 2.0:
            return RiskLevel.CRITICAL
        
        if cost_ratio >= 1.5:
            return RiskLevel.HIGH
        
        # ===== Override 风险评估 =====
        if override_count >= 8:
            return RiskLevel.CRITICAL
        
        if override_count >= 5:
            return RiskLevel.HIGH
        
        if override_count >= 3:
            return RiskLevel.MEDIUM
        
        if override_count >= 1:
            return RiskLevel.LOW
        
        return None
    
    def evaluate_with_reason(self, agent: str) -> tuple:
        """
        评估风险等级 + 原因
        
        Returns:
            (RiskLevel, reason) 或 (None, None)
        """
        events = self.repo.get_recent_events(agent)
        
        override_count = sum(
            1 for e in events 
            if e["type"] == "override"
        )
        
        cost_total = sum(
            e["value"] for e in events 
            if e["type"] == "cost"
        )
        
        budget = self.budget_config.get(agent, 50.0)
        cost_ratio = cost_total / budget if budget > 0 else 0
        
        # 成本风险
        if cost_ratio >= 2.0:
            return RiskLevel.CRITICAL, f"Cost exceeds 200% (${cost_total:.2f}/${budget:.2f})"
        
        if cost_ratio >= 1.5:
            return RiskLevel.HIGH, f"Cost exceeds 150% (${cost_total:.2f}/${budget:.2f})"
        
        # Override 风险
        if override_count >= 8:
            return RiskLevel.CRITICAL, f"Excessive overrides ({override_count})"
        
        if override_count >= 5:
            return RiskLevel.HIGH, f"High overrides ({override_count})"
        
        if override_count >= 3:
            return RiskLevel.MEDIUM, f"Multiple overrides ({override_count})"
        
        if override_count >= 1:
            return RiskLevel.LOW, f"Single override ({override_count})"
        
        return None, None
    
    def get_risk_summary(self, agent: str = None) -> dict:
        """获取风险摘要"""
        if agent:
            level = self.evaluate(agent)
            level_val, reason = self.evaluate_with_reason(agent)
            events = self.repo.get_recent_events(agent)
            
            return {
                "agent": agent,
                "level": level.value if level else "NORMAL",
                "reason": reason,
                "budget": self.budget_config.get(agent, 50.0),
                "cost": self.repo.get_total_cost(agent),
                "overrides": self.repo.get_event_count(agent, "override"),
                "is_blocked": self.repo.is_blocked(agent),
                "cooldown": self.repo.get_cooldown_remaining(agent),
                "recent_events": len(events)
            }
        
        # 全局
        agents = list(self.budget_config.keys())
        return {
            "agents": {a: self.evaluate(a).value if self.evaluate(a) else "NORMAL" for a in agents},
            "org_risk": self.repo.get_org_risk_level() or "NORMAL"
        }

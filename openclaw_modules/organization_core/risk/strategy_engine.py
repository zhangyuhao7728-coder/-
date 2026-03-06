"""
Strategy Engine
策略引擎 - 根据风险等级决定行动
"""

from organization_core.risk.risk_models import RiskLevel, RiskAction
from organization_core.risk.risk_repository import RiskRepository


class StrategyEngine:
    """策略引擎 - 风险应对决策"""
    
    # 冷却时间配置
    COOLDOWN_SECONDS = {
        RiskLevel.CRITICAL: 1800,   # 30分钟
        RiskLevel.HIGH: 600,        # 10分钟
        RiskLevel.MEDIUM: 300,     # 5分钟
        RiskLevel.LOW: 0,          # 无冷却
    }
    
    def __init__(self, risk_engine, repo: RiskRepository):
        self.risk_engine = risk_engine
        self.repo = repo
    
    def apply(self, agent: str) -> dict:
        """
        根据风险等级决定行动
        
        Args:
            agent: Agent 名称
            
        Returns:
            决策字典 {action, level, reason, cooldown}
        """
        # 1. 检查是否在冷却中
        if self.repo.is_blocked(agent):
            level = self.risk_engine.evaluate(agent)
            remaining = self.repo.get_cooldown_remaining(agent)
            return {
                "action": RiskAction.BLOCK.value,
                "level": level.value if level else "UNKNOWN",
                "reason": f"Cooldown active, {remaining}s remaining",
                "cooldown": remaining,
                "provider": None
            }
        
        # 2. 评估风险等级
        level = self.risk_engine.evaluate(agent)
        
        # 3. 无风险
        if level is None:
            return {
                "action": RiskAction.ALLOW.value,
                "level": "NORMAL",
                "reason": "No risk detected",
                "cooldown": 0,
                "provider": None
            }
        
        # 4. 根据等级采取行动
        if level == RiskLevel.CRITICAL:
            # 设置冷却
            cooldown = self.COOLDOWN_SECONDS[RiskLevel.CRITICAL]
            self.repo.set_cooldown(agent, cooldown)
            
            return {
                "action": RiskAction.BLOCK.value,
                "level": level.value,
                "reason": "CRITICAL risk - 30min cooldown",
                "cooldown": cooldown,
                "provider": None
            }
        
        if level == RiskLevel.HIGH:
            # 强制本地模型
            return {
                "action": RiskAction.FORCE_LOCAL.value,
                "level": level.value,
                "reason": "HIGH risk - forcing local model",
                "cooldown": 0,
                "provider": "local"
            }
        
        if level == RiskLevel.MEDIUM:
            # 限速
            return {
                "action": RiskAction.LIMIT.value,
                "level": level.value,
                "reason": "MEDIUM risk - rate limited",
                "cooldown": 0,
                "provider": None
            }
        
        if level == RiskLevel.LOW:
            # 记录但放行
            return {
                "action": RiskAction.ALLOW.value,
                "level": level.value,
                "reason": "LOW risk - allowed with warning",
                "cooldown": 0,
                "provider": None
            }
        
        return {
            "action": RiskAction.ALLOW.value,
            "level": "NORMAL",
            "reason": "Default allow",
            "cooldown": 0,
            "provider": None
        }
    
    def clear_cooldown(self, agent: str):
        """清除冷却"""
        self.repo.clear_cooldown(agent)
    
    def get_available_actions(self) -> dict:
        """获取所有可用的行动"""
        return {
            RiskAction.ALLOW.value: "正常放行",
            RiskAction.LIMIT.value: "限速处理",
            RiskAction.FORCE_LOCAL.value: "强制本地模型",
            RiskAction.BLOCK.value: "封锁 (冷却中)"
        }

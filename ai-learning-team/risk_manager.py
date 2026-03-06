"""
Risk Manager v2.0
风险管理系统 - 最终强化版
规则:
- 成本风险: >=200% CRITICAL, >=150% HIGH
- Override风险: >=8 CRITICAL, >=5 HIGH, >=3 MEDIUM, =1 LOW
- 优先级: CRITICAL > HIGH > MEDIUM > LOW (防止等级倒退)
"""

from datetime import datetime
from utils.risk_level import RiskLevel


class RiskManager:
    """风险管理器 v2.0"""
    
    def __init__(self, db, budget_config: dict = None):
        self.db = db
        self.budget_config = budget_config or {}
    
    # ======================
    # 主入口（线程安全）
    # ======================
    
    def check(self, agent_name: str):
        """
        检查风险（线程安全）
        
        Args:
            agent_name: Agent 名称
        """
        today = datetime.now().date().isoformat()
        
        # 获取今日数据
        cost = self.db.get_today_cost(agent_name)
        override_count = self.db.get_today_override_count(agent_name)
        budget = self.budget_config.get(agent_name, 50.0)
        
        # 评估风险
        level, reason = self._evaluate(cost, budget, override_count)
        
        if level is None:
            return
        
        # 获取今日最高已记录等级（防止等级倒退）
        existing_level = self._get_highest_today_level(agent_name, today)
        
        # 防止等级倒退：只记录更高或相等级别
        if existing_level and existing_level.value >= level.value:
            return
        
        # 原子写入（依赖 UNIQUE 约束）
        self._persist(
            date=today,
            agent_name=agent_name,
            level=level,
            cost=cost,
            budget=budget,
            override_count=override_count,
            reason=reason,
        )
    
    # ======================
    # 风险评估
    # ======================
    
    def _evaluate(self, cost: float, budget: float, override_count: int):
        """
        评估风险等级
        
        优先级: 成本风险 > Override风险
        """
        # 无效预算
        if budget <= 0:
            return RiskLevel.CRITICAL, "Invalid budget configuration"
        
        # 计算成本比率
        ratio = cost / budget if budget > 0 else 0
        
        # === 成本风险（最高优先级）===
        if ratio >= 2.0:
            return RiskLevel.CRITICAL, f"Cost exceeds 200% budget (${cost:.2f}/${budget:.2f})"
        
        if ratio >= 1.5:
            return RiskLevel.HIGH, f"Cost exceeds 150% budget (${cost:.2f}/${budget:.2f})"
        
        # === Override 风险 ===
        if override_count >= 8:
            return RiskLevel.CRITICAL, f"Excessive overrides (>={override_count})"
        
        if override_count >= 5:
            return RiskLevel.HIGH, f"High override frequency (>={override_count})"
        
        if override_count >= 3:
            return RiskLevel.MEDIUM, f"Multiple overrides (>={override_count})"
        
        if override_count == 1:
            return RiskLevel.LOW, "Single override"
        
        return None, None
    
    # ======================
    # 工具函数
    # ======================
    
    def _get_highest_today_level(self, agent: str, date: str):
        """获取今日最高风险等级"""
        rows = self.db.get_today_risk_levels(agent, date)
        
        if not rows:
            return None
        
        return max(
            [RiskLevel[level] for level in rows],
            key=lambda x: x.value
        )
    
    def _persist(self, date, agent_name, level, cost, budget, override_count, reason):
        """持久化风险事件"""
        self.db.insert_risk_event({
            "date": date,
            "agent_name": agent_name,
            "level": level.name,
            "cost": cost,
            "budget": budget,
            "override_count": override_count,
            "reason": reason,
            "created_at": datetime.now().isoformat(),
        })
        
        # 打印日志
        level_symbols = {
            "LOW": "⚠️",
            "MEDIUM": "⚠️⚠️",
            "HIGH": "🚨",
            "CRITICAL": "🛑"
        }
        
        print(f"{level_symbols.get(level.name, '❓')} Risk Alert [{level.name}] - {agent_name}: {reason}")
    
    # ======================
    # 锁检查
    # ======================
    
    def is_locked(self, agent_name: str) -> bool:
        """
        检查 Agent 是否被锁定
        
        CRITICAL 风险时返回 True
        """
        return self.db.is_agent_locked(agent_name)
    
    def get_budget(self, agent_name: str) -> float:
        """获取 Agent 预算"""
        return self.budget_config.get(agent_name, 50.0)
    
    def set_budget(self, agent_name: str, budget: float):
        """设置 Agent 预算"""
        self.budget_config[agent_name] = budget
    
    def get_risk_summary(self, agent_name: str = None) -> dict:
        """获取风险摘要"""
        events = self.db.get_risk_events(agent_name)
        
        summary = {
            "total": len(events),
            "by_level": {
                "LOW": 0,
                "MEDIUM": 0,
                "HIGH": 0,
                "CRITICAL": 0
            },
            "agents": {}
        }
        
        for event in events:
            level = event["level"]
            if level in summary["by_level"]:
                summary["by_level"][level] += 1
            
            agent = event["agent_name"]
            if agent not in summary["agents"]:
                summary["agents"][agent] = 0
            summary["agents"][agent] += 1
        
        return summary

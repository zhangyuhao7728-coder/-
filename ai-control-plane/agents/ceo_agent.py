#!/usr/bin/env python3
"""
CEO Agent - 决策Agent
继承自BaseAgent
"""
from base_agent import BaseAgent


class CEOAgent(BaseAgent):
    """CEO Agent - 决策者"""
    
    def __init__(self, router=None):
        super().__init__("CEO", "决策者", "qwen3.5:9b")
        self.router = router
    
    def decide(self, task: str, context: dict = None) -> str:
        """做决策"""
        self.tasks_completed += 1
        
        # 决策逻辑
        if "开发" in task or "创建" in task:
            decision = "批准开发计划，分配给Coder执行"
        elif "调研" in task or "分析" in task:
            decision = "批准调研计划，分配给Researcher执行"
        elif "检查" in task or "审核" in task:
            decision = "安排Reviewer进行审核"
        else:
            decision = "根据任务类型分配给合适Agent"
        
        return f"[CEO] 决策: {decision}"
    
    def review_team(self, team_stats: dict) -> str:
        """审核团队表现"""
        success_rate = team_stats.get("success_rate", 0)
        
        if success_rate >= 90:
            return "[CEO] 团队表现优秀，继续保持"
        elif success_rate >= 70:
            return "[CEO] 团队表现良好，有改进空间"
        else:
            return "[CEO] 需要关注团队表现，加强培训"


# 全局实例
_ceo = None

def get_ceo_agent(router=None) -> CEOAgent:
    global _ceo
    if _ceo is None:
        _ceo = CEOAgent(router)
    return _ceo

#!/usr/bin/env python3
"""
Reviewer Agent - 审核Agent
继承自BaseAgent
"""
from base_agent import BaseAgent


class ReviewerAgent(BaseAgent):
    """Reviewer Agent - 审核者"""
    
    def __init__(self, router=None):
        super().__init__("Reviewer", "审核者", "qwen3.5:9b")
        self.router = router
    
    def review(self, content: str) -> str:
        """审核"""
        self.tasks_completed += 1
        
        # 简单审核
        if len(content) < 10:
            return "[Reviewer] 内容过短，建议补充"
        
        return "[Reviewer] 审核通过"


# 全局实例
_reviewer = None

def get_reviewer_agent(router=None) -> ReviewerAgent:
    global _reviewer
    if _reviewer is None:
        _reviewer = ReviewerAgent(router)
    return _reviewer

"""
Token Manager - Token管理
"""

DAILY_LIMIT = 5_000_000      # 500万/天
PER_TASK_LIMIT = 50_000      # 5万/任务
PER_AGENT_LIMIT = 8_000      # 8千/Agent

class TokenManager:
    """Token管理器"""
    
    def __init__(self):
        self.daily_used = 0
        self.task_used = {}
    
    def can_use(self, tokens, task_id=None):
        """检查是否可以使用"""
        if self.daily_used + tokens > DAILY_LIMIT:
            return False
        if task_id:
            if self.task_used.get(task_id, 0) + tokens > PER_TASK_LIMIT:
                return False
        return True
    
    def use(self, tokens, task_id=None):
        """使用token"""
        self.daily_used += tokens
        if task_id:
            self.task_used[task_id] = self.task_used.get(task_id, 0) + tokens
    
    def reset_daily(self):
        """重置每日"""
        self.daily_used = 0
        self.task_used = {}
    
    def get_status(self):
        """获取状态"""
        return {
            "daily_used": self.daily_used,
            "daily_limit": DAILY_LIMIT,
            "usage_percent": f"{self.daily_used/DAILY_LIMIT*100:.1f}%"
        }

"""
Agent Scheduler - Agent调度器
安全限制
"""

MAX_AGENT_CALLS = 6
MAX_RECURSION = 2
MAX_TASK_RUNTIME = 120  # 秒

class Scheduler:
    def __init__(self):
        self.agent_calls = 0
        self.recursion_depth = 0
        self.task_start_time = None
    
    def can_call(self):
        return self.agent_calls < MAX_AGENT_CALLS
    
    def can_recurse(self):
        return self.recursion_depth < MAX_RECURSION
    
    def is_timeout(self):
        import time
        if not self.task_start_time:
            return False
        return time.time() - self.task_start_time > MAX_TASK_RUNTIME
    
    def reset(self):
        self.agent_calls = 0
        self.recursion_depth = 0

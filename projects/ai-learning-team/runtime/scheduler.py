"""Scheduler - 任务调度"""
MAX_CALLS = 6
MAX_TIME = 120

class Scheduler:
    def __init__(self):
        self.calls = 0
    
    def can_call(self): return self.calls < MAX_CALLS
    def increment(self): self.calls += 1
    def reset(self): self.calls = 0

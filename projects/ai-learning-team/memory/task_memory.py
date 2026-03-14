"""Task Memory - 当前任务"""
class TaskMemory:
    def __init__(self):
        self.current = None
    def store(self, t): self.current = t
    def get(self): return self.current

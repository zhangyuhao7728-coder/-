"""Task Memory - 当前任务"""
class TaskMemory:
    def __init__(self):
        self.current_task = None
    def store(self, task): self.current_task = task
    def get(self): return self.current_task

"""
Task Summary - 任务摘要
唯一进入LLM的任务信息
"""

class TaskSummary:
    def __init__(self):
        self.summary = {
            "goal": "",
            "progress": [],
            "next_step": ""
        }
    
    def update(self, goal=None, progress=None, next_step=None):
        if goal: self.summary["goal"] = goal
        if progress: self.summary["progress"] = progress
        if next_step: self.summary["next_step"] = next_step
    
    def get(self):
        """唯一进入LLM"""
        return self.summary

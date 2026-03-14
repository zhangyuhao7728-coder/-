"""
Task State - 任务状态
不进入LLM
"""

class TaskState:
    def __init__(self):
        self.state = {
            "task_id": None,
            "status": "IDLE",
            "current_step": None,
            "agent": None
        }
    
    def update(self, task_id=None, status=None, current_step=None, agent=None):
        if task_id: self.state["task_id"] = task_id
        if status: self.state["status"] = status
        if current_step: self.state["current_step"] = current_step
        if agent: self.state["agent"] = agent
    
    def get(self):
        """不返回给LLM"""
        return self.state
    
    def get_for_storage(self):
        """仅用于存储"""
        return self.state

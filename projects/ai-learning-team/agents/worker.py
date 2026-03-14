"""Worker Agent - 单一执行"""
ROLES = ["planner", "engineer", "reviewer", "analyst"]

class WorkerAgent:
    SYSTEM_PROMPT = "你是一个高效的执行Agent。只做当前任务推理，不保存历史。"
    
    def __init__(self):
        self.role = None
    
    def set_role(self, role):
        if role in ROLES:
            self.role = role
    
    def execute(self, task_summary, current_step, last_result):
        return {"status": "success", "role": self.role}

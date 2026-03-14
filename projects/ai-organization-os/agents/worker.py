"""
Worker Agent - 执行Agent
单次LLM调用完成
"""

SYSTEM_PROMPT = """
你是一个执行Agent。
只做当前任务推理，不保存历史。
"""

class WorkerAgent:
    """Worker Agent"""
    
    def __init__(self):
        self.role = None
        self.task = None
    
    def set_role(self, role):
        self.role = role
    
    def execute(self, task_summary, current_step, last_result):
        """执行任务"""
        context = {
            "role": self.role,
            "task_summary": task_summary,
            "current_step": current_step,
            "last_result": last_result
        }
        return {"status": "ready", "context": context}

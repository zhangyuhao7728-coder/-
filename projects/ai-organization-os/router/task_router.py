"""
Task Router - 任务路由器
只调用一次LLM
"""

def route(task):
    """
    路由任务到合适的Agent
    只调用一次LLM
    """
    task_type = task.get("type", "general")
    
    routers = {
        "code": "engineer",
        "research": "researcher",
        "review": "reviewer",
        "analysis": "analyst",
        "plan": "planner",
    }
    
    return routers.get(task_type, "worker")

class TaskRouter:
    """任务路由器类"""
    
    def __init__(self):
        self.routes = {
            "code": "engineer",
            "research": "researcher", 
            "review": "reviewer",
            "analysis": "analyst",
            "plan": "planner",
        }
    
    def route(self, task):
        task_type = task.get("type", "general")
        return self.routes.get(task_type, "worker")

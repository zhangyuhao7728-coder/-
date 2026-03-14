"""Task Router - 任务路由器"""
def route(task):
    """路由任务到合适的Agent"""
    task_type = task.get("type", "general")
    routes = {
        "plan": "planner",
        "code": "engineer",
        "review": "reviewer",
        "analysis": "analyst"
    }
    return routes.get(task_type, "worker")

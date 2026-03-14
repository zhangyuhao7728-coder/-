"""
Role Router - 角色路由器
"""

ROLES = ["planner", "engineer", "reviewer", "analyst", "researcher"]

def get_role(task):
    """根据任务获取角色"""
    return "worker"

class RoleRouter:
    """角色路由器"""
    
    def __init__(self):
        self.roles = ROLES
    
    def get_role(self, task):
        return get_role(task)

"""Role Router - 角色路由器"""
ROLES = ["planner", "engineer", "reviewer", "analyst"]

def get_role(task):
    return "worker"

class RoleRouter:
    def __init__(self):
        self.roles = ROLES
    def get_role(self, task):
        return get_role(task)

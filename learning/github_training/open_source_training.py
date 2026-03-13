#!/usr/bin/env python3
"""
Open Source Training - 开源项目训练
"""
import requests
from typing import Dict, List


class OpenSourceTraining:
    """开源项目训练"""
    
    # 推荐项目
    PROJECTS = {
        "requests": {
            "repo": "psf/requests",
            "description": "HTTP库",
            "level": "beginner",
            "focus": ["网络请求", "API调用"]
        },
        "flask": {
            "repo": "pallets/flask",
            "description": "Web框架",
            "level": "intermediate",
            "focus": ["Web开发", "路由", "模板"]
        },
        "fastapi": {
            "repo": "tiangolo/fastapi",
            "description": "现代API框架",
            "level": "intermediate",
            "focus": ["API", "异步", "类型提示"]
        },
        "django": {
            "repo": "django/django",
            "description": "全栈框架",
            "level": "advanced",
            "focus": ["ORM", "Admin", "认证"]
        },
        "numpy": {
            "repo": "numpy/numpy",
            "description": "数值计算",
            "level": "advanced",
            "focus": ["数组", "矩阵", "性能"]
        }
    }
    
    def __init__(self):
        self.fetcher = None
    
    def get_projects(self, level: str = None) -> List[Dict]:
        """获取项目列表"""
        projects = list(self.PROJECTS.values())
        
        if level:
            projects = [p for p in projects if p["level"] == level]
        
        return projects
    
    def get_project(self, name: str) -> Dict:
        """获取项目信息"""
        return self.PROJECTS.get(name, {})
    
    def create_learning_task(self, project_name: str) -> Dict:
        """创建学习任务"""
        
        project = self.get_project(project_name)
        
        if not project:
            return {"error": "项目不存在"}
        
        # 生成学习任务
        tasks = [
            f"1. 克隆并阅读 {project['repo']} 源码",
            "2. 理解项目结构和主要模块",
            "3. 找到一个核心功能并深入理解",
            "4. 尝试模仿实现类似功能",
            "5. 提交自己的改进"
        ]
        
        return {
            "project": project["repo"],
            "description": project["description"],
            "focus": project["focus"],
            "level": project["level"],
            "tasks": tasks
        }


_training = None

def get_open_source_training():
    global _training
    if _training is None:
        _training = OpenSourceTraining()
    return _training

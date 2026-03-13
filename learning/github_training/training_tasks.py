#!/usr/bin/env python3
"""
Training Tasks - 训练任务
"""
from typing import Dict, List
from github_training.repo_fetcher import get_repo_fetcher
from github_training.project_analyzer import get_project_analyzer


class TrainingTasks:
    """GitHub训练任务"""
    
    # 推荐仓库
    REPOS = {
        "beginner": [
            "psf/requests",
            "django/django",
            "pandas-dev/pandas"
        ],
        "intermediate": [
            "tensorflow/tensorflow",
            "pytorch/pytorch",
            "scikit-learn/scikit-learn"
        ],
        "advanced": [
            "ansible/ansible",
            "celery/celery",
            "matplotlib/matplotlib"
        ]
    }
    
    def __init__(self):
        self.fetcher = get_repo_fetcher()
        self.analyzer = get_project_analyzer()
        self.completed = []
    
    def get_recommended(self, level: str = "beginner") -> List[Dict]:
        """获取推荐仓库"""
        
        repos = self.REPOS.get(level, self.REPOS["beginner"])
        
        recommendations = []
        for repo in repos:
            info = self.fetcher.fetch_repo(repo)
            
            if "error" not in info:
                recommendations.append({
                    "name": info.get("full_name"),
                    "description": info.get("description"),
                    "stars": info.get("stargazers_count"),
                    "language": info.get("language")
                })
        
        return recommendations
    
    def create_task(self, repo: str) -> Dict:
        """创建学习任务"""
        
        info = self.fetcher.fetch_repo(repo)
        
        if "error" in info:
            return {"error": info["error"]}
        
        files = self.fetcher.get_python_files(repo)
        
        task = {
            "repo": repo,
            "description": info.get("description"),
            "stars": info.get("stargazers_count"),
            "files_count": len(files),
            "steps": [
                f"1. 阅读 {repo} 的README",
                "2. 了解项目结构",
                "3. 选择一个核心模块学习",
                "4. 尝试理解关键函数",
                "5. 模仿写类似代码"
            ]
        }
        
        return task
    
    def analyze_repo(self, repo: str) -> Dict:
        """分析仓库"""
        
        files = self.fetcher.get_python_files(repo)
        
        # 简化：只返回基本信息
        return {
            "repo": repo,
            "python_files": len(files),
            "files": files[:10]
        }


_tasks = None

def get_training_tasks() -> TrainingTasks:
    global _tasks
    if _tasks is None:
        _tasks = TrainingTasks()
    return _tasks


# 测试
if __name__ == "__main__":
    tasks = get_training_tasks()
    
    print("=== GitHub训练任务测试 ===\n")
    
    # 推荐
    recs = tasks.get_recommended("beginner")
    print(f"推荐仓库: {len(recs)}")
    
    for r in recs[:2]:
        print(f"  - {r['name']}: {r['stars']}⭐")

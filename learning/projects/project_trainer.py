#!/usr/bin/env python3
"""
Project Trainer - 自动项目训练
"""
from typing import Dict, List


class ProjectTrainer:
    """项目训练器"""
    
    # 初级项目
    BEGINNER_PROJECTS = [
        {
            "id": "todo_cli",
            "name": "CLI待办应用",
            "description": "命令行待办事项管理",
            "skills": ["Python基础", "文件操作"],
            "difficulty": 1,
            "time": "2小时"
        },
        {
            "id": "password_generator",
            "name": "密码生成器",
            "description": "生成随机安全密码",
            "skills": ["字符串操作", "随机数"],
            "difficulty": 1,
            "time": "1小时"
        },
        {
            "id": "calculator",
            "name": "计算器",
            "description": "简单计算器",
            "skills": ["函数", "异常处理"],
            "difficulty": 1,
            "time": "1小时"
        }
    ]
    
    # 中级项目
    INTERMEDIATE_PROJECTS = [
        {
            "id": "web_api",
            "name": "REST API",
            "description": "Flask RESTful API",
            "skills": ["Flask", "JSON", "HTTP"],
            "difficulty": 2,
            "time": "4小时"
        },
        {
            "id": "web_scraper",
            "name": "网页爬虫",
            "description": "抓取网页数据",
            "skills": ["Requests", "BeautifulSoup"],
            "difficulty": 2,
            "time": "3小时"
        },
        {
            "id": "file_manager",
            "name": "文件管理器",
            "description": "图形化文件管理",
            "skills": ["GUI", "os模块"],
            "difficulty": 2,
            "time": "4小时"
        }
    ]
    
    # 高级项目
    ADVANCED_PROJECTS = [
        {
            "id": "ai_chatbot",
            "name": "AI聊天机器人",
            "description": "基于API的对话机器人",
            "skills": ["API集成", "NLP"],
            "difficulty": 3,
            "time": "8小时"
        },
        {
            "id": "task_scheduler",
            "name": "任务调度器",
            "description": "定时任务管理系统",
            "skills": ["异步", "调度"],
            "difficulty": 3,
            "time": "6小时"
        },
        {
            "id": "mini_search_engine",
            "name": "迷你搜索引擎",
            "description": "简单搜索引擎",
            "skills": ["索引", "排序"],
            "difficulty": 3,
            "time": "10小时"
        }
    ]
    
    def __init__(self):
        self.completed = []
    
    def get_projects(self, level: str) -> List[Dict]:
        """获取项目列表"""
        
        if level == "beginner":
            return self.BEGINNER_PROJECTS
        elif level == "intermediate":
            return self.INTERMEDIATE_PROJECTS
        elif level == "advanced":
            return self.ADVANCED_PROJECTS
        else:
            return self.BEGINNER_PROJECTS
    
    def get_all(self) -> Dict:
        """获取所有项目"""
        return {
            "beginner": self.BEGINNER_PROJECTS,
            "intermediate": self.INTERMEDIATE_PROJECTS,
            "advanced": self.ADVANCED_PROJECTS
        }
    
    def start_project(self, project_id: str) -> Dict:
        """开始项目"""
        
        all_projects = self.BEGINNER_PROJECTS + self.INTERMEDIATE_PROJECTS + self.ADVANCED_PROJECTS
        
        for p in all_projects:
            if p["id"] == project_id:
                return {
                    "started": True,
                    "project": p,
                    "steps": self._generate_steps(p)
                }
        
        return {"started": False, "error": "项目不存在"}
    
    def _generate_steps(self, project: Dict) -> List[str]:
        """生成项目步骤"""
        
        steps = [
            f"1. 设计项目结构",
            "2. 实现核心功能",
            "3. 添加错误处理",
            "4. 测试和调试",
            "5. 优化代码"
        ]
        
        return steps
    
    def complete_project(self, project_id: str):
        """完成项目"""
        self.completed.append(project_id)


_trainer = None

def get_project_trainer() -> ProjectTrainer:
    global _trainer
    if _trainer is None:
        _trainer = ProjectTrainer()
    return _trainer


# 测试
if __name__ == "__main__":
    trainer = get_project_trainer()
    
    print("=== 项目训练测试 ===\n")
    
    print("初级项目:")
    for p in trainer.get_projects("beginner"):
        print(f"  - {p['name']}: {p['description']}")
    
    print("\n中级项目:")
    for p in trainer.get_projects("intermediate"):
        print(f"  - {p['name']}")

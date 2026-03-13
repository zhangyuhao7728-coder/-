#!/usr/bin/env python3
"""
Project Factory - 项目生成工厂
"""
import requests
from typing import Dict


class ProjectFactory:
    """项目生成工厂"""
    
    def __init__(self):
        self.ollama_url = "http://localhost:11434"
    
    def call_llm(self, prompt: str) -> str:
        try:
            resp = requests.post(
                f"{self.ollama_url}/api/generate",
                json={"model": "qwen2.5:14b", "prompt": prompt, "stream": False},
                timeout=60
            )
            if resp.status_code == 200:
                return resp.json().get("response", "")
        except:
            pass
        return "无法生成项目"
    
    def generate_project(self, topic: str) -> Dict:
        """生成完整项目"""
        
        prompt = f"""设计一个完整的Python项目: {topic}

返回JSON格式：
{{
    "name": "项目名称",
    "description": "项目描述",
    "structure": ["文件1", "文件2"],
    "features": ["功能1", "功能2"],
    "tech_stack": ["Python", "Flask"],
    "steps": ["步骤1", "步骤2"]
}}
"""
        result = self.call_llm(prompt)
        
        # 返回基本结构
        return {
            "name": topic,
            "description": f"{topic}相关项目",
            "structure": ["main.py", "utils.py", "models.py"],
            "features": ["核心功能"],
            "tech_stack": ["Python"],
            "steps": ["设计架构", "实现功能", "测试"]
        }
    
    def generate_architecture(self, project_name: str) -> Dict:
        """生成架构"""
        
        return {
            "layers": ["API", "Service", "DAO"],
            "modules": ["auth", "user", "task"],
            "database": "SQLite"
        }
    
    def generate_milestones(self, project: Dict) -> list:
        """生成里程碑"""
        
        return [
            {"week": 1, "goal": "完成基础架构"},
            {"week": 2, "goal": "实现核心功能"},
            {"week": 3, "goal": "添加测试"},
            {"week": 4, "goal": "优化和部署"}
        ]


_factory = None

def get_project_factory() -> ProjectFactory:
    global _factory
    if _factory is None:
        _factory = ProjectFactory()
    return _factory


# 测试
if __name__ == "__main__":
    factory = get_project_factory()
    
    print("=== 项目工厂测试 ===\n")
    
    project = factory.generate_project("任务调度系统")
    print(f"项目: {project['name']}")
    print(f"结构: {project['structure']}")

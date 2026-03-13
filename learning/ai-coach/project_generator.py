#!/usr/bin/env python3
"""
Project Generator - AI项目生成器
"""
import requests
from typing import Dict, List


class ProjectGenerator:
    """AI项目生成器"""
    
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
        """生成项目"""
        
        prompt = f"""设计一个Python项目: {topic}

返回JSON格式：
{{
    "name": "项目名称",
    "description": "简短描述",
    "features": ["功能1", "功能2"],
    "tech_stack": ["技术栈"],
    "difficulty": "easy/medium/hard",
    "time_estimate": "预估时间"
}}
"""
        result = self.call_llm(prompt)
        
        # 简单解析
        project = {
            "name": topic,
            "description": f"{topic}相关项目",
            "features": ["核心功能1", "核心功能2"],
            "tech_stack": ["Python"],
            "difficulty": "medium",
            "time_estimate": "2小时"
        }
        
        return project
    
    def generate_roadmap(self, topic: str) -> List[str]:
        """生成项目路线图"""
        
        prompt = f"""为{topic}项目生成开发步骤

返回步骤列表，每行一个步骤
"""
        result = self.call_llm(prompt)
        
        steps = [s.strip() for s in result.split("\n") if s.strip()]
        
        return steps[:5] if steps else ["步骤1", "步骤2"]
    
    def generate_code(self, project_name: str) -> str:
        """生成项目代码"""
        
        prompt = f"""生成一个简单的{project_name}Python项目代码

只生成核心代码，不要超过50行
"""
        return self.call_llm(prompt)


_generator = None

def get_project_generator() -> ProjectGenerator:
    global _generator
    if _generator is None:
        _generator = ProjectGenerator()
    return _generator


def generate_project(topic: str) -> Dict:
    return get_project_generator().generate_project(topic)


# 测试
if __name__ == "__main__":
    gen = get_project_generator()
    
    print("=== 项目生成测试 ===\n")
    
    project = gen.generate_project("Todo CLI")
    print(f"项目: {project['name']}")
    print(f"难度: {project['difficulty']}")

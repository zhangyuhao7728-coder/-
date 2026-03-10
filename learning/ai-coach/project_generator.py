#!/usr/bin/env python3
"""
🚀 项目生成器
自动生成Python实战项目
"""

import random
import json
from pathlib import Path

class ProjectGenerator:
    def __init__(self):
        self.projects = {
            "beginner": {
                "CLI工具": [
                    {
                        "name": "待办事项CLI",
                        "description": "命令行待办事项管理器",
                        "features": ["添加任务", "删除任务", "完成任务", "查看列表"],
                        "skills": ["列表操作", "文件读写", "命令行参数"]
                    },
                    {
                        "name": "计算器",
                        "description": "支持加减乘除的计算器",
                        "features": ["基本运算", "历史记录", "清除历史"],
                        "skills": ["函数", "条件判断", "循环"]
                    },
                    {
                        "name": "猜数字游戏",
                        "description": "1-100猜数字游戏",
                        "features": ["随机数生成", "次数限制", "排行榜"],
                        "skills": ["随机数", "循环", "条件判断"]
                    }
                ],
                "自动化": [
                    {
                        "name": "文件整理器",
                        "description": "按类型自动整理文件",
                        "features": ["扫描目录", "分类移动", "生成报告"],
                        "skills": ["os模块", "shutil模块", "路径处理"]
                    }
                ]
            },
            "intermediate": {
                "API": [
                    {
                        "name": "天气查询CLI",
                        "description": "调用天气API查询天气",
                        "features": ["城市查询", "预报展示", "历史记录"],
                        "skills": ["requests库", "JSON处理", "API调用"]
                    },
                    {
                        "name": "RESTful API",
                        "description": "使用Flask/FastAPI构建API",
                        "features": ["增删改查", "数据库集成", "用户认证"],
                        "skills": ["Flask/FastAPI", "RESTful", "数据库"]
                    }
                ],
                "数据处理": [
                    {
                        "name": "CSV分析器",
                        "description": "分析CSV数据文件",
                        "features": ["数据统计", "图表生成", "导出报告"],
                        "skills": ["pandas", "matplotlib", "数据分析"]
                    }
                ]
            },
            "advanced": {
                "AI": [
                    {
                        "name": "AI聊天机器人",
                        "description": "对接LLM API的聊天机器人",
                        "features": ["对话管理", "上下文记忆", "多角色"],
                        "skills": ["API调用", "prompt工程", "流式输出"]
                    },
                    {
                        "name": "文档问答系统",
                        "description": "基于RAG的问答系统",
                        "features": ["文档读取", "向量存储", "相似度搜索"],
                        "skills": ["langchain", "向量数据库", "文本处理"]
                    }
                ]
            }
        }
    
    def generate(self, level="beginner", category=None):
        """生成项目"""
        levels = self.projects
        
        if level not in levels:
            level = "beginner"
        
        if category and category in levels[level]:
            projects = levels[level][category]
        else:
            # 随机选择
            all_projects = []
            for cat, projs in levels[level].items():
                all_projects.extend(projs)
            projects = all_projects
        
        project = random.choice(projects)
        
        return {
            "level": level,
            "name": project["name"],
            "description": project["description"],
            "features": project["features"],
            "skills": project["skills"],
            "steps": self._generate_steps(project)
        }
    
    def _generate_steps(self, project):
        """生成项目步骤"""
        return [
            "1. 项目初始化",
            "2. 核心功能实现",
            "3. 添加错误处理",
            "4. 优化用户体验",
            "5. 测试和文档"
        ]
    
    def list_projects(self):
        """列出所有项目"""
        for level, categories in self.projects.items():
            print(f"\n{'='*40}")
            print(f"📁 {level.upper()}")
            print("=" * 40)
            
            for category, projects in categories.items():
                print(f"\n📂 {category}:")
                for p in projects:
                    print(f"  • {p['name']}: {p['description']}")

def main():
    generator = ProjectGenerator()
    
    print("🚀 项目生成器")
    print("=" * 40)
    
    # 生成一个项目
    project = generator.generate("beginner")
    
    print(f"\n项目: {project['name']}")
    print(f"描述: {project['description']}")
    print(f"\n功能:")
    for f in project['features']:
        print(f"  ✓ {f}")
    print(f"\n需要技能:")
    for s in project['skills']:
        print(f"  • {s}")

if __name__ == "__main__":
    main()

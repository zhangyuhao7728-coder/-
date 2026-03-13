#!/usr/bin/env python3
"""
Project Analyzer - 项目分析器
"""
import re
from typing import Dict, List


class ProjectAnalyzer:
    """项目分析"""
    
    def analyze(self, files: List[str], contents: Dict[str, str]) -> Dict:
        """分析项目"""
        
        stats = {
            "files": len(files),
            "functions": 0,
            "classes": 0,
            "imports": set(),
            "tech_stack": []
        }
        
        for path, content in contents.items():
            # 统计函数
            stats["functions"] += len(re.findall(r"def \w+\(", content))
            
            # 统计类
            stats["classes"] += len(re.findall(r"class \w+:", content))
            
            # 导入
            imports = re.findall(r"^import (\w+)", content, re.M)
            imports += re.findall(r"^from (\w+) import", content, re.M)
            stats["imports"].update(imports)
        
        # 技术栈
        stats["tech_stack"] = self._detect_tech_stack(stats["imports"])
        
        return stats
    
    def _detect_tech_stack(self, imports: set) -> List[str]:
        """检测技术栈"""
        
        tech_map = {
            "flask": "Flask",
            "django": "Django",
            "fastapi": "FastAPI",
            "requests": "Requests",
            "numpy": "NumPy",
            "pandas": "Pandas",
            "torch": "PyTorch",
            "tensorflow": "TensorFlow",
            "sklearn": "scikit-learn",
            "pytest": "pytest",
            "aiohttp": "aiohttp",
            "sqlalchemy": "SQLAlchemy"
        }
        
        found = []
        for imp in imports:
            if imp.lower() in tech_map:
                found.append(tech_map[imp.lower()])
        
        return found
    
    def extract_structure(self, content: str) -> Dict:
        """提取结构"""
        
        functions = re.findall(r"def (\w+)\((.*?)\):", content)
        classes = re.findall(r"class (\w+)(?:\(.*?\))?:", content)
        
        return {
            "functions": [{"name": f[0], "args": f[1]} for f in functions],
            "classes": classes
        }
    
    def suggest_learning(self, stats: Dict) -> List[str]:
        """建议学习内容"""
        
        suggestions = []
        
        if "Flask" in stats.get("tech_stack", []):
            suggestions.append("学习Flask路由和模板")
        
        if "Django" in stats.get("tech_stack", []):
            suggestions.append("学习Django ORM")
        
        if "requests" in [i.lower() for i in stats.get("imports", [])]:
            suggestions.append("学习HTTP请求库使用")
        
        if stats["classes"] > 5:
            suggestions.append("学习面向对象设计模式")
        
        return suggestions


_analyzer = None

def get_project_analyzer() -> ProjectAnalyzer:
    global _analyzer
    if _analyzer is None:
        _analyzer = ProjectAnalyzer()
    return _analyzer

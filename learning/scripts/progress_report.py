#!/usr/bin/env python3
"""
📈 学习进度报告
"""

import json
from pathlib import Path

BASE_DIR = Path("~/项目/Ai学习系统/learning").expanduser()
STATS_FILE = BASE_DIR / "learning-data" / "stats.json"

def load_stats():
    """加载统计数据"""
    if STATS_FILE.exists():
        with open(STATS_FILE) as f:
            return json.load(f)
    return {
        "python_basics": 0,
        "python_advanced": 0,
        "algorithms": 0,
        "ai_ml": 0,
        "data_skills": 0,
        "problems_solved": 0,
        "projects_completed": 0,
        "total_study_time": 0
    }

def calculate_progress(stats):
    """计算总体进度"""
    weights = {
        "python_basics": 20,
        "python_advanced": 20,
        "algorithms": 20,
        "ai_ml": 20,
        "data_skills": 20
    }
    
    total = sum(stats.get(k, 0) * w for k, w in weights.items()) / 100
    return min(total, 100)

def show_progress():
    """显示进度"""
    stats = load_stats()
    progress = calculate_progress(stats)
    
    print("=" * 50)
    print("📈 学习进度总览")
    print("=" * 50)
    
    # 进度条
    bar_length = 30
    filled = int(bar_length * progress / 100)
    bar = "█" * filled + "░" * (bar_length - filled)
    
    print(f"\n[{bar}] {progress:.1f}%")
    
    # 各领域进度
    areas = [
        ("Python基础", stats.get("python_basics", 0)),
        ("Python进阶", stats.get("python_advanced", 0)),
        ("算法", stats.get("algorithms", 0)),
        ("AI/ML", stats.get("ai_ml", 0)),
        ("数据技能", stats.get("data_skills", 0))
    ]
    
    print("\n📚 各领域进度:")
    for name, value in areas:
        bar_len = 15
        filled = int(bar_len * value / 100)
        bar = "▓" * filled + "░" * (bar_len - filled)
        print(f"  {name:12s} [{bar}] {value}%")
    
    # 成就统计
    print("\n🏆 成就:")
    print(f"  • 完成题目: {stats.get('problems_solved', 0)}题")
    print(f"  • 完成项目: {stats.get('projects_completed', 0)}个")
    print(f"  • 总学习时长: {stats.get('total_study_time', 0)}分钟")
    
    # 下一个目标
    print("\n🎯 下一个目标:")
    if stats.get("python_basics", 0) < 100:
        print("  → 完成Python基础")
    elif stats.get("algorithms", 0) < 50:
        print("  → 算法练习达到50%")
    else:
        print("  → 继续AI/ML学习")
    
    print("=" * 50)

if __name__ == "__main__":
    show_progress()

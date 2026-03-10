#!/usr/bin/env python3
"""
📊 每周学习总结
"""

import json
from pathlib import Path
from datetime import datetime, timedelta

BASE_DIR = Path("~/项目/Ai学习系统/learning").expanduser()
DATA_DIR = BASE_DIR / "learning-data"

def get_week_range():
    """获取本周日期范围"""
    today = datetime.now()
    start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=6)
    return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")

def load_weekly_data():
    """加载本周数据"""
    stats_file = DATA_DIR / "stats.json"
    if stats_file.exists():
        with open(stats_file) as f:
            return json.load(f)
    return {}

def generate_weekly_report():
    """生成周报"""
    start_date, end_date = get_week_range()
    data = load_weekly_data()
    
    report = {
        "week": f"{start_date} ~ {end_date}",
        "summary": {
            "total_problems": data.get("problems_solved", 0),
            "concepts_learned": data.get("concepts_learned", 0),
            "projects_completed": data.get("projects_completed", 0),
            "study_time_minutes": data.get("study_time", 0)
        },
        "details": {
            "python_basics": f"{data.get('python_basics', 0)}%",
            "algorithms": f"{data.get('algorithms', 0)}%",
            "ai_ml": f"{data.get('ai_ml', 0)}%"
        },
        "achievements": [],
        "improvements": []
    }
    
    # 生成成就
    if report["summary"]["total_problems"] >= 20:
        report["achievements"].append("🏆 算法达人: 完成20+题")
    if report["summary"]["study_time_minutes"] >= 300:
        report["achievements"].append("⏰ 学习标兵: 300+分钟")
    
    # 生成改进建议
    if data.get("python_basics", 0) < 50:
        report["improvements"].append("建议加强Python基础")
    if data.get("algorithms", 0) < 30:
        report["improvements"].append("算法练习需要加强")
    
    return report

def show_report():
    """显示周报"""
    report = generate_weekly_report()
    
    print("=" * 50)
    print(f"📊 本周学习总结 - {report['week']}")
    print("=" * 50)
    
    print("\n📈 学习数据:")
    s = report["summary"]
    print(f"  • 完成题目: {s['total_problems']}题")
    print(f"  • 学习概念: {s['concepts_learned']}个")
    print(f"  • 完成项目: {s['projects_completed']}个")
    print(f"  • 学习时长: {s['study_time_minutes']}分钟")
    
    print("\n📚 进度:")
    for k, v in report["details"].items():
        print(f"  • {k}: {v}")
    
    if report["achievements"]:
        print("\n🏆 成就:")
        for a in report["achievements"]:
            print(f"  {a}")
    
    if report["improvements"]:
        print("\n💡 改进建议:")
        for i in report["improvements"]:
            print(f"  • {i}")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    show_report()

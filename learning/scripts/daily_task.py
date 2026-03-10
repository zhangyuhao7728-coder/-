#!/usr/bin/env python3
"""
📅 每日学习任务自动生成系统
"""

import json
import random
from pathlib import Path
from datetime import datetime

# 路径配置
BASE_DIR = Path("~/项目/Ai学习系统/learning").expanduser()
DATA_DIR = BASE_DIR / "learning-data"
TASKS_FILE = DATA_DIR / "daily" / "tasks.json"

# 任务题库
TASK_BANK = {
    "python-basics": {
        "变量与数据类型": ["创建变量练习", "数据类型转换"],
        "运算符": ["算术运算练习", "比较运算"],
        "条件语句": ["if-else练习", "多条件判断"],
        "循环": ["for循环", "while循环", "循环嵌套"],
    },
    "algorithms": {
        "两数之和": ["哈希表解法", "暴力枚举"],
        "回文数": ["字符串反转", "数学方法"],
        "二分查找": ["基础二分", "左边界", "右边界"],
    },
    "python-advanced": {
        "列表操作": ["列表推导式", "切片操作"],
        "字典操作": ["字典遍历", " defaultdict"],
    }
}

# 每日目标
DAILY_GOAL = {
    "concepts": 2,    # 学习2个知识点
    "exercises": 3,    # 做3道题
    "project": 1,      # 1个项目任务
    "time": 60,        # 60分钟
}

def load_progress():
    """加载学习进度"""
    stats_file = DATA_DIR / "stats.json"
    if stats_file.exists():
        with open(stats_file) as f:
            return json.load(f)
    return {
        "python_basics": 0,
        "algorithms": 0,
        "ai_ml": 0,
        "problems_solved": 0
    }

def generate_daily_tasks():
    """生成每日任务"""
    progress = load_progress()
    
    # 根据进度选择任务
    if progress.get("python_basics", 0) < 50:
        focus = "python-basics"
    elif progress.get("algorithms", 0) < 30:
        focus = "algorithms"
    else:
        focus = random.choice(["python-basics", "algorithms"])
    
    tasks = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "focus": focus,
        "daily_goal": DAILY_GOAL,
        "tasks": []
    }
    
    # 生成知识点学习任务
    concepts = TASK_BANK.get(focus, {})
    concept_names = list(concepts.keys())[:DAILY_GOAL["concepts"]]
    for name in concept_names:
        tasks["tasks"].append({
            "type": "concept",
            "topic": name,
            "subtasks": random.choice(concepts[name]),
            "estimated_time": 20
        })
    
    # 生成算法题任务
    for i in range(DAILY_GOAL["exercises"]):
        difficulty = "easy" if i < 2 else "medium"
        tasks["tasks"].append({
            "type": "exercise",
            "difficulty": difficulty,
            "estimated_time": 15
        })
    
    # 生成项目任务
    tasks["tasks"].append({
        "type": "project",
        "topic": random.choice(["待办CLI", "计算器", "猜数字"]),
        "estimated_time": 30
    })
    
    return tasks

def save_tasks(tasks):
    """保存任务"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "daily").mkdir(exist_ok=True)
    
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def show_tasks():
    """显示今日任务"""
    if TASKS_FILE.exists():
        with open(TASKS_FILE) as f:
            tasks = json.load(f)
    else:
        tasks = generate_daily_tasks()
        save_tasks(tasks)
    
    print("=" * 40)
    print(f"📅 今日任务 - {tasks['date']}")
    print(f"🎯 重点: {tasks['focus']}")
    print("=" * 40)
    
    for i, task in enumerate(tasks["tasks"], 1):
        if task["type"] == "concept":
            print(f"{i}. 📖 学习: {task['topic']} - {task['subtasks']}")
        elif task["type"] == "exercise":
            print(f"{i}. 💻 练习: {task['difficulty']}难度算法题")
        else:
            print(f"{i}. 🚀 项目: {task['topic']}")
    
    print("=" * 40)
    print(f"⏱️  目标时长: {tasks['daily_goal']['time']}分钟")

def main():
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--generate":
        tasks = generate_daily_tasks()
        save_tasks(tasks)
        print("✅ 今日任务已生成!")
    
    show_tasks()

if __name__ == "__main__":
    main()

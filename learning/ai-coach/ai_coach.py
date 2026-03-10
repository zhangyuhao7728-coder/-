#!/usr/bin/env python3
"""
🤖 AI学习教练
根据用户水平推荐学习内容
"""

import json
from pathlib import Path

class AICoach:
    def __init__(self, learning_dir):
        self.learning_dir = Path(learning_dir)
        self.progress_file = self.learning_dir / "learning-data" / "stats.json"
        self.load_progress()
    
    def load_progress(self):
        """加载学习进度"""
        if self.progress_file.exists():
            with open(self.progress_file) as f:
                self.stats = json.load(f)
        else:
            self.stats = {
                "python_basics": 0,
                "python_advanced": 0,
                "algorithms": 0,
                "ai_ml": 0,
                "data_skills": 0,
                "problems_solved": 0,
                "projects_completed": 0
            }
    
    def save_progress(self):
        """保存进度"""
        self.progress_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.progress_file, "w") as f:
            json.dump(self.stats, f, indent=2)
    
    def get_recommendation(self):
        """获取学习推荐"""
        scores = {
            "python_basics": self.stats.get("python_basics", 0),
            "python_advanced": self.stats.get("python_advanced", 0),
            "algorithms": self.stats.get("algorithms", 0),
        }
        
        # 找到最低分
        weakest = min(scores, key=scores.get)
        
        recommendations = {
            "python_basics": "📖 建议学习Python基础: curriculum/python-basics/variables.md",
            "python_advanced": "📖 建议学习Python进阶: curriculum/python-advanced/",
            "algorithms": "💻 建议练习算法: problems/easy/two_sum/",
        }
        
        return {
            "当前进度": self.stats,
            "建议": recommendations.get(weakest, "继续加油!"),
            "下一步": self.get_next_topic(weakest)
        }
    
    def get_next_topic(self, weak_area):
        """获取下一个学习主题"""
        topics = {
            "python_basics": [
                "variables.md",
                "loops.md", 
                "functions.md",
                "classes.md"
            ],
            "python_advanced": [
                "decorators.md",
                "generators.md",
                "async.md"
            ],
            "algorithms": [
                "problems/easy/two_sum/",
                "problems/easy/palindrome/",
                "problems/medium/longest_substring/"
            ]
        }
        
        current = self.stats.get(f"{weak_area}_current", 0)
        topic_list = topics.get(weak_area, [])
        
        if current < len(topic_list):
            return f"下一章: {topic_list[current]}"
        return "已完成本阶段!"
    
    def update_progress(self, area, score):
        """更新进度"""
        key = f"{area}_progress"
        self.stats[key] = score
        self.stats["last_update"] = str(Path(".").stat().st_mtime)
        self.save_progress()

if __name__ == "__main__":
    coach = AICoach("~/项目/Ai学习系统/learning")
    print("🤖 AI学习教练")
    print("=" * 30)
    rec = coach.get_recommendation()
    for k, v in rec.items():
        print(f"\n{k}:")
        print(f"  {v}")

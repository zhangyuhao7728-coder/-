#!/usr/bin/env python3
"""
🧠 AI学习分析器
自动分析弱项，调整训练难度
"""

import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

BASE_DIR = Path("~/项目/Ai学习系统/learning").expanduser()
STATS_FILE = BASE_DIR / "learning-data" / "stats.json"

class AIAnalyzer:
    def __init__(self):
        self.load_data()
    
    def load_data(self):
        """加载学习数据"""
        if STATS_FILE.exists():
            with open(STATS_FILE) as f:
                self.data = json.load(f)
        else:
            self.data = {"skills": {}, "weaknesses": [], "strengths": []}
    
    def save_data(self):
        """保存数据"""
        STATS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(STATS_FILE, "w") as f:
            json.dump(self.data, f, indent=2)
    
    def analyze_accuracy(self):
        """分析正确率"""
        results = defaultdict(lambda: {"correct": 0, "total": 0})
        
        for skill_name, skill_data in self.data.get("skills", {}).items():
            topics = skill_data.get("topics", {})
            for topic_name, topic_data in topics.items():
                correct = topic_data.get("correct", 0)
                total = topic_data.get("attempts", 0)
                if total > 0:
                    accuracy = correct / total
                    results[f"{skill_name}.{topic_name}"] = {
                        "correct": correct,
                        "total": total,
                        "accuracy": accuracy
                    }
        
        return results
    
    def find_weaknesses(self):
        """找出弱项 (正确率 < 60%)"""
        analysis = self.analyze_accuracy()
        weaknesses = []
        
        for key, data in analysis.items():
            if data["accuracy"] < 0.6 and data["total"] >= 3:
                weaknesses.append({
                    "topic": key,
                    "accuracy": data["accuracy"],
                    "attempts": data["total"],
                    "priority": 1 - data["accuracy"]  # 越低越优先
                })
        
        # 按优先级排序
        weaknesses.sort(key=lambda x: x["priority"], reverse=True)
        return weaknesses
    
    def find_strengths(self):
        """找出强项 (正确率 >= 80%)"""
        analysis = self.analyze_accuracy()
        strengths = []
        
        for key, data in analysis.items():
            if data["accuracy"] >= 0.8 and data["total"] >= 3:
                strengths.append({
                    "topic": key,
                    "accuracy": data["accuracy"],
                    "attempts": data["total"]
                })
        
        return strengths
    
    def get_recommended_difficulty(self, topic):
        """根据表现推荐难度"""
        # 基础：easy
        # 正确率>=80%: medium
        # 正确率>=90%: hard
        # 正确率<60%: easy
        # 正确率<40%: 重新学习
        
        analysis = self.analyze_accuracy()
        if topic in analysis:
            accuracy = analysis[topic]["accuracy"]
            if accuracy >= 0.9:
                return "hard"
            elif accuracy >= 0.8:
                return "medium"
            elif accuracy >= 0.6:
                return "easy"
            else:
                return "review"  # 需要复习
        return "easy"  # 默认
    
    def generate_recommendations(self):
        """生成个性化推荐"""
        weaknesses = self.find_weaknesses()
        strengths = self.find_strengths()
        
        recommendations = {
            "weaknesses": weaknesses[:3],  # Top 3 弱项
            "strengths": strengths[:3],
            "daily_focus": [],
            "next_level": "easy",
            "study_plan": []
        }
        
        # 每日重点学习弱项
        for w in weaknesses[:2]:
            recommendations["daily_focus"].append({
                "topic": w["topic"],
                "action": "加强练习",
                "difficulty": "easy"
            })
        
        # 生成学习计划
        if weaknesses:
            recommendations["study_plan"] = [
                {"day": 1, "topic": weaknesses[0]["topic"], "type": "复习"},
                {"day": 2, "topic": weaknesses[0]["topic"], "type": "练习"},
                {"day": 3, "topic": weaknesses[1]["topic"] if len(weaknesses) > 1 else "巩固", "type": "练习"}
            ]
        
        return recommendations
    
    def update_progress(self, topic, correct):
        """更新进度"""
        # 解析 topic (格式: skill.topic)
        parts = topic.split(".")
        if len(parts) >= 2:
            skill = parts[0]
            topic_name = parts[1]
            
            if skill not in self.data["skills"]:
                self.data["skills"][skill] = {"topics": {}}
            
            if topic_name not in self.data["skills"][skill]["topics"]:
                self.data["skills"][skill]["topics"][topic_name] = {
                    "attempts": 0,
                    "correct": 0
                }
            
            self.data["skills"][skill]["topics"][topic_name]["attempts"] += 1
            if correct:
                self.data["skills"][skill]["topics"][topic_name]["correct"] += 1
            
            self.save_data()
    
    def analyze_and_report(self):
        """综合分析报告"""
        weaknesses = self.find_weaknesses()
        strengths = self.find_strengths()
        recommendations = self.generate_recommendations()
        
        return {
            "analysis_time": datetime.now().isoformat(),
            "weaknesses": weaknesses,
            "strengths": strengths,
            "recommendations": recommendations
        }

def main():
    analyzer = AIAnalyzer()
    
    print("=" * 50)
    print("🧠 AI 学习分析报告")
    print("=" * 50)
    
    report = analyzer.analyze_and_report()
    
    # 显示弱项
    print("\n📉 弱项分析:")
    if report["weaknesses"]:
        for w in report["weaknesses"]:
            print(f"  • {w['topic']}: {w['accuracy']*100:.0f}% 正确率 ({w['attempts']}次)")
    else:
        print("  暂无明显弱项，继续加油!")
    
    # 显示强项
    print("\n📈 强项:")
    if report["strengths"]:
        for s in report["strengths"]:
            print(f"  ✅ {s['topic']}: {s['accuracy']*100:.0f}% 正确率")
    else:
        print("  暂无强项记录")
    
    # 今日建议
    print("\n💡 今日建议:")
    rec = report["recommendations"]
    if rec["daily_focus"]:
        for f in rec["daily_focus"]:
            print(f"  → 重点学习: {f['topic']} ({f['action']})")
    else:
        print("  → 继续保持，当前学习进度良好!")
    
    print("\n" + "=" * 50)
    
    return report

if __name__ == "__main__":
    main()

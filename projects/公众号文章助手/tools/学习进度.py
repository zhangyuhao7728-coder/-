#!/usr/bin/env python3
"""AI学习进度追踪"""
import json
from datetime import datetime

class LearningTracker:
    def __init__(self):
        self.db_file = 'data/学习进度.json'
        self.data = self.load()
    
    def load(self):
        import os
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r') as f:
                return json.load(f)
        return {
            'python': {'progress': 60, 'topics': []},
            'ai': {'progress': 30, 'topics': []},
            'project': {'progress': 50, 'topics': []}
        }
    
    def add_progress(self, category, topic, percent):
        if category not in self.data:
            self.data[category] = {'progress': 0, 'topics': []}
        self.data[category]['topics'].append({
            'topic': topic,
            'percent': percent,
            'date': datetime.now().isoformat()
        })
        self.data[category]['progress'] = percent
        
        with open(self.db_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def report(self):
        print("="*50)
        print("📚 AI学习进度")
        print("="*50)
        for cat, data in self.data.items():
            bar = "█" * (data['progress'] // 10) + "░" * (10 - data['progress'] // 10)
            print(f"\n{cat:12} [{bar}] {data['progress']}%")

if __name__ == '__main__':
    tracker = LearningTracker()
    tracker.report()

#!/usr/bin/env python3
"""
AI任务CLI - 通过命令行调用AI完成任务
"""
import os
import sys
import json
from datetime import datetime

class AITaskCLI:
    def __init__(self):
        self.task_dir = "~/项目/Ai学习系统/projects/公众号文章助手/tasks"
        self.task_dir = os.path.expanduser(self.task_dir)
        os.makedirs(self.task_dir, exist_ok=True)
    
    def create_task(self, task, priority="normal"):
        """创建任务"""
        task_id = datetime.now().strftime("%Y%m%d%H%M%S")
        
        task_data = {
            "id": task_id,
            "task": task,
            "priority": priority,
            "status": "pending",
            "created": datetime.now().isoformat()
        }
        
        filename = f"{self.task_dir}/{task_id}.json"
        with open(filename, 'w') as f:
            json.dump(task_data, f, ensure_ascii=False, indent=2)
        
        return task_id
    
    def list_tasks(self):
        """列出所有任务"""
        tasks = []
        for f in os.listdir(self.task_dir):
            if f.endswith('.json'):
                with open(f"{self.task_dir}/{f}") as f:
                    tasks.append(json.load(f))
        return tasks
    
    def run(self):
        if len(sys.argv) < 2:
            print("""
╔══════════════════════════════════════════╗
║         🚀 AI任务助手 CLI               ║
╠══════════════════════════════════════════╣
║  用法:                                  ║
║    ai-task "任务描述"                   ║
║    ai-task --list                       ║
║    ai-task --help                       ║
╚══════════════════════════════════════════╝
            """)
            return
        
        cmd = sys.argv[1]
        
        if cmd == "--list":
            tasks = self.list_tasks()
            print(f"\n📋 任务列表 ({len(tasks)}个):\n")
            for t in tasks:
                print(f"  [{t['status']}] {t['task'][:50]}...")
        
        elif cmd == "--help":
            print("""
帮助:
  ai-task "任务描述"   - 创建新任务
  ai-task --list       - 列出所有任务
  ai-task --help       - 显示帮助
            """)
        
        else:
            # 整个参数作为任务
            task = " ".join(sys.argv[1:])
            task_id = self.create_task(task)
            print(f"\n✅ 任务已创建: {task_id}")
            print(f"   任务: {task}")

if __name__ == "__main__":
    cli = AITaskCLI()
    cli.run()

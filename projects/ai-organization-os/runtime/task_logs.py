"""
Task Logs - 任务日志
不进入LLM
"""

import os

class TaskLogs:
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self.logs = {}
    
    def add(self, agent, log):
        """添加日志"""
        if agent not in self.logs:
            self.logs[agent] = []
        self.logs[agent].append(log)
    
    def save(self):
        """保存到文件"""
        for agent, entries in self.logs.items():
            with open(f"{self.log_dir}/{agent}.log", "a") as f:
                f.write("\n".join(str(e) for e in entries) + "\n")
    
    def get(self, agent):
        """不返回给LLM"""
        return self.logs.get(agent, [])

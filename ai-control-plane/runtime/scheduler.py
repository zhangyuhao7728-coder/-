#!/usr/bin/env python3
"""
Runtime Scheduler - 运行时调度器
"""
import time
from datetime import datetime, timedelta
from typing import Callable, Dict, List


class RuntimeScheduler:
    """运行时调度器"""
    
    def __init__(self):
        self.tasks = []
        self.running = False
    
    def schedule(self, task: Callable, interval: int, name: str = ""):
        """调度任务"""
        self.tasks.append({
            "task": task,
            "interval": interval,
            "name": name,
            "last_run": 0,
        })
    
    def run_once(self, delay: int, task: Callable, name: str = ""):
        """一次性任务"""
        self.tasks.append({
            "task": task,
            "delay": delay,
            "name": name,
            "type": "once",
        })
    
    def start(self):
        """启动"""
        self.running = True
        
        while self.running:
            now = time.time()
            
            for t in self.tasks:
                if t.get("type") == "once":
                    if t.get("delay", 0) > 0:
                        time.sleep(t["delay"])
                        t["task"]()
                        self.tasks.remove(t)
                else:
                    interval = t.get("interval", 60)
                    last = t.get("last_run", 0)
                    
                    if now - last >= interval:
                        try:
                            t["task"]()
                        except Exception as e:
                            print(f"Task error: {e}")
                        t["last_run"] = now
            
            time.sleep(1)
    
    def stop(self):
        self.running = False


# 全局实例
_scheduler = None

def get_runtime_scheduler() -> RuntimeScheduler:
    global _scheduler
    if _scheduler is None:
        _scheduler = RuntimeScheduler()
    return _scheduler

#!/usr/bin/env python3
"""
Auto Tasks - 自动任务系统
每天自动执行任务
"""
import time
from datetime import datetime
from typing import Callable, Dict


class AutoTask:
    """自动任务"""
    
    def __init__(self, name: str, task: Callable, interval: int, enabled: bool = True):
        self.name = name
        self.task = task
        self.interval = interval  # 秒
        self.enabled = enabled
        self.last_run = None
        self.run_count = 0
    
    def should_run(self) -> bool:
        """是否应该运行"""
        if not self.enabled:
            return False
        
        if self.last_run is None:
            return True
        
        elapsed = time.time() - self.last_run
        return elapsed >= self.interval
    
    def run(self):
        """运行"""
        try:
            self.task()
            self.last_run = time.time()
            self.run_count += 1
            print(f"✅ 自动任务完成: {self.name} (第{self.run_count}次)")
        except Exception as e:
            print(f"❌ 自动任务失败: {self.name} - {e}")


class AutoTaskManager:
    """自动任务管理器"""
    
    def __init__(self):
        self.tasks = {}
        self.running = False
    
    def add(self, name: str, task: Callable, interval: int, 
            description: str = ""):
        """添加自动任务"""
        auto_task = AutoTask(name, task, interval)
        self.tasks[name] = auto_task
        
        print(f"⏰ 添加自动任务: {name}")
        print(f"   间隔: {interval}秒")
        print(f"   说明: {description}")
        
        return auto_task
    
    def enable(self, name: str):
        """启用"""
        if name in self.tasks:
            self.tasks[name].enabled = True
            print(f"✅ 启用: {name}")
    
    def disable(self, name: str):
        """禁用"""
        if name in self.tasks:
            self.tasks[name].enabled = False
            print(f"⏸ 禁用: {name}")
    
    def run(self):
        """运行所有自动任务"""
        for name, task in self.tasks.items():
            if task.should_run():
                task.run()
    
    def run_once(self, name: str):
        """运行单个任务"""
        if name in self.tasks:
            self.tasks[name].run()
    
    def start(self):
        """启动循环"""
        self.running = True
        print("\n🚀 自动任务系统启动\n")
        
        while self.running:
            self.run()
            time.sleep(10)  # 每10秒检查一次
    
    def stop(self):
        """停止"""
        self.running = False
        print("\n🛑 自动任务系统停止")


# ===== 预设自动任务 =====

def task_fetch_ai_news():
    """任务1: 抓取AI新闻"""
    print("\n📰 抓取AI新闻...")
    # 这里可以调用爬虫
    print("   完成")


def task_analyze_trend():
    """任务2: 分析趋势"""
    print("\n📊 分析趋势...")
    # 这里可以分析数据
    print("   完成")


def task_update_knowledge():
    """任务3: 更新知识库"""
    print("\n📚 更新知识库...")
    # 这里可以更新知识
    print("   完成")


def task_health_check():
    """任务4: 健康检查"""
    print("\n🏥 健康检查...")
    import requests
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=5)
        print(f"   Ollama: {'✅' if r.status_code==200 else '❌'}")
    except:
        print("   Ollama: ❌")


# ===== 创建系统 =====

def create_auto_tasks() -> AutoTaskManager:
    """创建自动任务系统"""
    manager = AutoTaskManager()
    
    # 添加预设任务
    manager.add(
        "ai_news",
        task_fetch_ai_news,
        3600,  # 每小时
        "抓取AI新闻"
    )
    
    manager.add(
        "analyze_trend",
        task_analyze_trend,
        7200,  # 每2小时
        "分析趋势"
    )
    
    manager.add(
        "update_knowledge",
        task_update_knowledge,
        86400,  # 每天
        "更新知识库"
    )
    
    manager.add(
        "health_check",
        task_health_check,
        300,  # 每5分钟
        "系统健康检查"
    )
    
    return manager


# 测试
if __name__ == "__main__":
    print("=== Auto Tasks 测试 ===\n")
    
    # 创建
    manager = create_auto_tasks()
    
    # 运行一次
    print("\n运行健康检查:")
    manager.run_once("health_check")
    
    # 统计
    print("\n任务统计:")
    for name, task in manager.tasks.items():
        print(f"  {name}: {task.run_count}次")

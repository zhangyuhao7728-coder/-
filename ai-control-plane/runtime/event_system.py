#!/usr/bin/env python3
"""
Event System - 事件驱动系统
响应Telegram/定时任务/文件变化/系统监控
"""
import time
from datetime import datetime, timedelta
from typing import Callable, Dict, List
from enum import Enum


class EventType(Enum):
    """事件类型"""
    TELEGRAM = "telegram"          # Telegram消息
    SCHEDULED = "scheduled"       # 定时任务
    FILE_CHANGED = "file_changed"  # 文件变化
    SYSTEM = "system"            # 系统事件
    WEBHOOK = "webhook"          # Webhook
    MANUAL = "manual"            # 手动触发


class Event:
    """事件"""
    
    def __init__(self, event_type: EventType, data: Dict = None):
        self.type = event_type
        self.data = data or {}
        self.timestamp = datetime.now()
        self.source = self.data.get("source", "unknown")
    
    def __repr__(self):
        return f"<Event {self.type.value} from {self.source}>"


class EventSystem:
    """事件系统"""
    
    def __init__(self):
        self.handlers = {}  # 事件处理器
        self.event_history = []  # 事件历史
        self.scheduled_tasks = []  # 定时任务
    
    def on(self, event_type: EventType, handler: Callable):
        """注册事件处理器"""
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        
        self.handlers[event_type].append(handler)
        print(f"✅ 注册处理器: {event_type.value}")
    
    def emit(self, event: Event):
        """触发事件"""
        print(f"\n📢 事件: {event}")
        
        # 记录历史
        self.event_history.append(event)
        if len(self.event_history) > 100:
            self.event_history.pop(0)
        
        # 调用处理器
        handlers = self.handlers.get(event.type, [])
        
        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                print(f"❌ 处理器错误: {e}")
    
    # ===== Telegram事件 =====
    
    def handle_telegram(self, message: str, user_id: str):
        """处理Telegram消息"""
        event = Event(EventType.TELEGRAM, {
            "message": message,
            "user_id": user_id,
            "source": f"telegram:{user_id}"
        })
        self.emit(event)
    
    # ===== 定时任务 =====
    
    def schedule(self, interval: int, task: Callable, name: str = ""):
        """添加定时任务"""
        self.scheduled_tasks.append({
            "name": name,
            "interval": interval,
            "task": task,
            "last_run": 0,
        })
        print(f"⏰ 定时任务: {name} (每{interval}秒)")
    
    def run_scheduled(self):
        """运行定时任务"""
        now = time.time()
        
        for task_info in self.scheduled_tasks:
            interval = task_info["interval"]
            last = task_info["last_run"]
            
            if now - last >= interval:
                try:
                    task_info["task"]()
                    task_info["last_run"] = now
                except Exception as e:
                    print(f"❌ 定时任务错误: {e}")
    
    # ===== 文件变化 =====
    
    def watch_file(self, filepath: str):
        """监听文件变化 (简化版)"""
        import os
        
        if not hasattr(self, "_file_mtimes"):
            self._file_mtimes = {}
        
        try:
            mtime = os.path.getmtime(filepath)
            
            if filepath not in self._file_mtimes:
                self._file_mtimes[filepath] = mtime
            elif mtime != self._file_mtimes[filepath]:
                # 文件变化
                self._file_mtimes[filepath] = mtime
                
                event = Event(EventType.FILE_CHANGED, {
                    "filepath": filepath,
                    "source": "filesystem"
                })
                self.emit(event)
        except:
            pass
    
    # ===== 系统监控 =====
    
    def check_system(self):
        """系统健康检查"""
        import requests
        
        # 检查Ollama
        try:
            r = requests.get("http://localhost:11434/api/tags", timeout=3)
            if r.status_code != 200:
                event = Event(EventType.SYSTEM, {
                    "service": "ollama",
                    "status": "down",
                    "source": "health_check"
                })
                self.emit(event)
        except:
            event = Event(EventType.SYSTEM, {
                "service": "ollama",
                "status": "offline",
                "source": "health_check"
            })
            self.emit(event)
    
    # ===== 历史 =====
    
    def get_history(self, n: int = 10) -> List[Event]:
        """获取事件历史"""
        return self.event_history[-n:]
    
    def print_history(self):
        """打印事件历史"""
        print("\n📜 事件历史:")
        for e in self.get_history(5):
            print(f"  {e.timestamp.strftime('%H:%M:%S')} | {e.type.value} | {e.source}")


# 全局实例
_event_system = None

def get_event_system() -> EventSystem:
    global _event_system
    if _event_system is None:
        _event_system = EventSystem()
    return _event_system


# 测试
if __name__ == "__main__":
    print("=== Event System 测试 ===\n")
    
    events = get_event_system()
    
    # 注册处理器
    def handle_telegram_event(event):
        print(f"   处理Telegram: {event.data.get('message')}")
    
    events.on(EventType.TELEGRAM, handle_telegram_event)
    
    # 触发事件
    events.handle_telegram("写一个爬虫", "123456")
    
    # 定时任务
    events.schedule(60, lambda: print("⏰ 执行定时任务"), "test_task")
    
    # 历史
    events.print_history()

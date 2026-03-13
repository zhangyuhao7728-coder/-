#!/usr/bin/env python3
"""
Event Loop - 事件循环
"""
import time
from typing import Callable, Dict, List


class EventLoop:
    """事件循环"""
    
    def __init__(self):
        self.running = False
        self.handlers = {}
        self.events = []
    
    def register(self, event_type: str, handler: Callable):
        """注册处理器"""
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)
    
    def emit(self, event_type: str, data: Dict = None):
        """触发事件"""
        event = {
            "type": event_type,
            "data": data or {},
            "timestamp": time.time(),
        }
        self.events.append(event)
        
        # 执行处理器
        handlers = self.handlers.get(event_type, [])
        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                print(f"Handler error: {e}")
    
    def start(self):
        """启动循环"""
        self.running = True
    
    def stop(self):
        """停止循环"""
        self.running = False
    
    def get_events(self, n: int = 10) -> List[Dict]:
        return self.events[-n:]


# 全局实例
_loop = None

def get_event_loop() -> EventLoop:
    global _loop
    if _loop is None:
        _loop = EventLoop()
    return _loop

"""
Event Bus
负责系统内部事件流转
"""

from typing import Callable, Dict, List


class EventBus:
    def __init__(self) -> None:
        self._subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, handler: Callable) -> None:
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

    def publish(self, event_type: str, data: dict) -> None:
        handlers = self._subscribers.get(event_type, [])
        for handler in handlers:
            handler(data)

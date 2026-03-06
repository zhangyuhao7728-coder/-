"""
Test Core
测试 Organization Core 核心功能
"""

from organization_core.event_bus import EventBus
from organization_core.scheduler import Scheduler
from organization_core.state_manager import StateManager


def test_event_bus():
    """测试事件总线"""
    bus = EventBus()
    
    received = []
    
    def handler(data):
        received.append(data)
    
    bus.subscribe("test_event", handler)
    bus.publish("test_event", {"msg": "hello"})
    
    assert len(received) == 1
    assert received[0]["msg"] == "hello"
    print("✅ EventBus 测试通过")


def test_scheduler():
    """测试调度器"""
    scheduler = Scheduler()
    
    # 测试各种消息类型
    test_cases = [
        ("请帮我制定一个计划", "planner"),
        ("帮我研究一下这个问题", "researcher"),
        ("请写代码实现这个功能", "engineer"),
        ("帮我审查这段代码的质量", "reviewer"),
        ("分析一下这个数据", "analyst"),
        ("你好，今天怎么样", "ceo"),
    ]
    
    for message, expected in test_cases:
        result = scheduler.decide({"content": message})
        assert result == expected, f"Expected {expected}, got {result}"
    
    print("✅ Scheduler 测试通过")


def test_state_manager():
    """测试状态管理器"""
    state = StateManager()
    
    state.set("user", "zhangyuhao")
    state.set("count", 42)
    
    assert state.get("user") == "zhangyuhao"
    assert state.get("count") == 42
    assert state.get("nonexistent") is None
    
    state.delete("count")
    assert state.get("count") is None
    
    print("✅ StateManager 测试通过")


def main():
    print("🚀 开始测试 Organization Core...\n")
    
    test_event_bus()
    test_scheduler()
    test_state_manager()
    
    print("\n🎉 所有测试通过！")


if __name__ == "__main__":
    main()

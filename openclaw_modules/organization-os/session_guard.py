"""
Session Guard - 防 Context 爆炸
集成 ContextManager 自动压缩
"""

import json
import os

# 导入 ContextManager
from context_manager import ContextManager

# 初始化
ctx_manager = ContextManager(max_ratio=0.7)

SESSION_FILE = "session.json"


def load():
    """加载会话数据"""
    if not os.path.exists(SESSION_FILE):
        return {"history": [], "max_context": 200000, "used_tokens": 0}
    
    with open(SESSION_FILE) as f:
        return json.load(f)


def save(data):
    """保存会话数据"""
    with open(SESSION_FILE, "w") as f:
        json.dump(data, f)


def guard():
    """
    会话保护：
    超过 40 条消息时，保留前 15 条摘要
    超过 70% context 时，自动压缩
    """
    session = load()
    
    # 方法1: 消息数保护
    history = session.get("history", [])
    
    if len(history) > 40:
        summary = history[:15]
        session["history"] = summary
        print(f"🛡️ Session compressed: {len(history)} → {len(summary)} messages")
        save(session)
        return True
    
    # 方法2: Context 比例保护
    used = session.get("used_tokens", 0)
    max_ctx = session.get("max_context", 200000)
    ratio = used / max_ctx if max_ctx > 0 else 0
    
    if ratio > 0.7:
        session = ctx_manager.compress(session)
        print(f"🛡️ Context compressed: {ratio:.1%} → 40%")
        save(session)
        return True
    
    return False


def protect(session):
    """
    保护会话（供外部调用）
    
    Args:
        session: 会话字典
        
    Returns:
        保护后的 session
    """
    return ctx_manager.check(session)


def add_message(msg: dict):
    """添加消息"""
    session = load()
    session.setdefault("history", []).append(msg)
    session["used_tokens"] = len(json.dumps(session["history"]))
    save(session)


def get_count() -> int:
    """获取消息数量"""
    session = load()
    return len(session.get("history", []))


# ===== 测试 =====

if __name__ == "__main__":
    print("="*50)
    print("Session Guard + Context Manager Test")
    print("="*50)
    
    session = {
        "history": [{"role": "user", "content": f"Message {i}"} for i in range(50)],
        "used_tokens": 150000,
        "max_context": 200000
    }
    
    print(f"📊 Before: {len(session['history'])} messages, {session['used_tokens']} tokens")
    
    # 保护
    result = protect(session)
    print(f"🛡️ Protected: {result}")
    
    print(f"📊 After: {len(session['history'])} messages, {session['used_tokens']} tokens")

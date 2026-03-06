"""
Context Manager - 上下文管理器
自动压缩对话历史，防止 Context 爆炸
"""

class ContextManager:
    """上下文管理器"""
    
    def __init__(self, max_ratio=0.7):
        """
        初始化
        
        Args:
            max_ratio: 最大使用比例 (0.7 = 70%)
        """
        self.max_ratio = max_ratio
    
    def check(self, session):
        """
        检查并处理上下文
        
        Args:
            session: 会话对象
            
        Returns:
            处理后的 session
        """
        used = session.get("used_tokens", 0)
        max_ctx = session.get("max_context", 200000)
        
        ratio = used / max_ctx
        
        if ratio > self.max_ratio:
            print(f"⚠️ Context ratio {ratio:.1%} > {self.max_ratio:.1%}, compressing...")
            return self.compress(session)
        
        return session
    
    def compress(self, session):
        """
        压缩会话历史
        
        保留前半部分 + 摘要，释放空间
        """
        history = session.get("history", [])
        
        if not history:
            return session
        
        # 保留前半部分
        keep_count = len(history) // 2
        kept = history[:keep_count]
        
        # 创建摘要
        summary = history[keep_count:]
        summary_text = self._create_summary(summary)
        
        # 重构历史
        session["history"] = [
            {"role": "system", "content": "Conversation summary: " + summary_text}
        ] + kept
        
        # 重新计算 token
        session["used_tokens"] = int(session.get("max_context", 200000) * 0.4)
        
        print(f"✅ Compressed: {len(history)} → {len(session['history'])} messages")
        
        return session
    
    def _create_summary(self, messages):
        """创建摘要"""
        if not messages:
            return "No recent messages"
        
        # 简单摘要：取最近几条
        count = min(5, len(messages))
        recent = messages[-count:]
        
        return f"Recent {count} messages about: " + ", ".join([
            m.get("role", "user") for m in recent
        ])
    
    def get_status(self, session):
        """获取状态"""
        used = session.get("used_tokens", 0)
        max_ctx = session.get("max_context", 200000)
        ratio = used / max_ctx
        
        return {
            "used": used,
            "max": max_ctx,
            "ratio": ratio,
            "level": "healthy" if ratio < 0.5 else "warning" if ratio < 0.7 else "critical"
        }


# ===== 测试 =====

if __name__ == "__main__":
    print("="*40)
    print("Context Manager Test")
    print("="*40)
    
    manager = ContextManager(max_ratio=0.7)
    
    # 模拟会话
    session = {
        "used_tokens": 150000,
        "max_context": 200000,
        "history": [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi!"},
            {"role": "user", "content": "How are you?"},
            {"role": "assistant", "content": "I'm good"},
            {"role": "user", "content": "Tell me about AI"},
            {"role": "assistant", "content": "AI is..."},
            {"role": "user", "content": "What is Python?"},
            {"role": "assistant", "content": "Python is..."},
        ]
    }
    
    # 检查状态
    status = manager.get_status(session)
    print(f"\n📊 Before: {status}")
    
    # 压缩
    session = manager.check(session)
    
    # 再次检查
    status = manager.get_status(session)
    print(f"\n📊 After: {status}")
    print(f"\n📝 History: {len(session['history'])} messages")

"""
Agent Bus - Agent 通信
支持：私聊、群聊、任务推进
"""

import queue


class AgentBus:
    """Agent 消息总线"""
    
    def __init__(self):
        self.queues = {}
    
    def register(self, name):
        """注册 Agent"""
        self.queues[name] = queue.Queue()
    
    def send(self, src, dst, msg):
        """发送消息"""
        if dst in self.queues:
            self.queues[dst].put({
                "from": src,
                "msg": msg
            })
            print(f"📨 {src} → {dst}: {msg}")
    
    def receive(self, name):
        """接收消息"""
        q = self.queues.get(name)
        if q and not q.empty():
            return q.get()
        return None
    
    def broadcast(self, src, msg):
        """群聊：广播消息给所有 Agent"""
        for dst in self.queues.keys():
            if dst != src:
                self.send(src, dst, msg)


# ===== 测试 =====

if __name__ == "__main__":
    print("="*40)
    print("Agent Bus Test")
    print("="*40)
    
    bus = AgentBus()
    
    # 注册
    bus.register("ceo")
    bus.register("engineer")
    bus.register("team")
    
    # 私聊
    print("\n💬 Private Message:")
    bus.send("ceo", "engineer", "写一个爬虫")
    
    # 群聊
    print("\n📢 Broadcast:")
    bus.broadcast("engineer", "代码写完了")
    
    # 接收
    print("\n📥 Receiving:")
    msg = bus.receive("engineer")
    print(f"  Engineer got: {msg}")

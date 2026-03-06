# 🤖 Agent 机器人连接状态

## 当前配置

| Agent | Token | 连接状态 |
|-------|-------|----------|
| **planner** | 8673494887:AAGLudy2Y69vUZTnPi9U4ndLFSY6jE-VdwQ | ⏳ 待测试 |
| **researcher** | 8779180935:AAFIrUuEAe7up1T6UN7KOLLVHz9GqNQgZvY | ⏳ 待测试 |
| **engineer** | 8791760022:AAGwCGs8_BJg9BqGd3hhyzwGZhOm9DMa4i0 | ⏳ 待测试 |

---

## 测试脚本

```bash
#!/bin/bash
# test_agents.sh

BOT_TOKEN="TOKEN_HERE"
CHAT_ID="YOUR_CHAT_ID"

# 发送测试消息
curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
  -d "chat_id=${CHAT_ID}&text=Hello from Agent"
```

---

## 下一步

1. 给每个 Agent 的机器人发送 /start
2. 测试消息发送
3. 配置 Agent 响应规则

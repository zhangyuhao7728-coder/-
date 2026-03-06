# 飞书多机器人配置

## 已分配 (Telegram)

| Agent | Telegram Bot Token | 状态 |
|-------|-------------------|------|
| planner | 8673494887:AAGLudy2Y69vUZTnPi9U4ndLFSY6jE-VdwQ | ✅ |
| researcher | 8779180935:AAFIrUuEAe7up1T6UN7KOLLVHz9GqNQgZvY | ✅ |

## 待分配 (飞书)

| Agent | 飞书 App ID | 飞书 App Secret | 状态 |
|-------|-------------|-----------------|------|
| engineer | [待填写] | [待填写] | ⏳ |
| reviewer | [待填写] | [待填写] | ⏳ |
| analyst | [待填写] | [待填写] | ⏳ |

---

## 快速配置脚本

```bash
# 运行配置脚本
cd ai-learning-team
./scripts/feishu_config.sh engineer <APP_ID> <APP_SECRET> <TOKEN>
./scripts/feishu_config.sh reviewer <APP_ID> <APP_SECRET> <TOKEN>
./scripts/feishu_config.sh analyst <APP_ID> <APP_SECRET> <TOKEN>
```

---

## 飞书应用创建步骤

1. 访问 https://open.feishu.cn/
2. 创建企业自建应用
3. 添加权限：
   - im:message:send_as_bot
   - im:message:patch
   - im:chat:create
   - contact:contact.base
4. 发布应用
5. 获取凭证并运行配置脚本

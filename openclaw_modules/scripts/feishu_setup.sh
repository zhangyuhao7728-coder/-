#!/bin/bash

# =============================================================================
# 飞书多机器人配置脚本
# 为 AI 学习团队的每个 Agent 创建独立的飞书机器人
# =============================================================================

echo "🤖 飞书多机器人配置向导"
echo "========================"
echo ""

# =============================================================================
# 配置区域 - 在此填入 Agent 信息
# =============================================================================

# 团队成员列表
AGENTS=(
  "planner:任务规划师"
  "researcher:调研研究员"
  "engineer:工程师"
  "reviewer:审查员"
  "analyst:分析师"
)

# =============================================================================
# 飞书应用配置模板 (所有 Agent 使用相同权限)
# =============================================================================

# 权限列表
PERMISSIONS=(
  "contact:contact.base"
  "im:message:send_as_bot"
  "im:message:patch"
  "im:message:delete"
  "im:chat:create"
  "im:chat:update"
  "im:chat:member"
  "im:chat:leave"
  "approval:instance:create"
  "approval:instance:approve"
  "approval:definition:readonly"
  "calendar:calendar:readonly"
  "calendar:event:readonly"
  "drive:drive:readonly"
  "drive:file:readonly"
)

# =============================================================================
# 应用配置 (需在飞书开放平台手动创建)
# =============================================================================

# 每个 Agent 需要在飞书开放平台创建应用并填写以下信息：
echo "📋 每个 Agent 需要手动创建的应用信息："
echo ""
for agent_info in "${AGENTS[@]}"; do
  IFS=':' read -r id name <<< "$agent_info"
  echo "  - ${name} (${id}):"
  echo "    * App ID:  "
  echo "    * App Secret: "
  echo "    * Verification Token: "
  echo ""
done

# =============================================================================
# 自动配置脚本模板
# =============================================================================

cat > /Users/zhangyuhao/zhangyuhao/python/ai-learning-team/scripts/feishu_config.sh << 'SCRIPT'
#!/bin/bash

# -----------------------------------------------------------------------------
# 飞书机器人自动配置脚本
# 使用方法: ./feishu_config.sh <AGENT_ID> <APP_ID> <APP_SECRET> <VERIFICATION_TOKEN>
# -----------------------------------------------------------------------------

AGENT_ID=$1
APP_ID=$2
APP_SECRET=$3
VERIFICATION_TOKEN=$4

if [ -z "$AGENT_ID" ] || [ -z "$APP_ID" ]; then
  echo "❌ 参数不足"
  echo "用法: ./feishu_config.sh <AGENT_ID> <APP_ID> <APP_SECRET> <VERIFICATION_TOKEN>"
  exit 1
fi

echo "🤖 配置 ${AGENT_ID} 飞书机器人..."
echo "  App ID: ${APP_ID}"

# -----------------------------------------------------------------------------
# 1. 获取 tenant_access_token
# -----------------------------------------------------------------------------
echo ""
echo "📡 Step 1: 获取访问令牌..."

TOKEN_RESPONSE=$(curl -s -X POST 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' \
  -H 'Content-Type: application/json' \
  -d "{
    \"app_id\": \"${APP_ID}\",
    \"app_secret\": \"${APP_SECRET}\"
  }")

TENANT_TOKEN=$(echo $TOKEN_RESPONSE | jq -r '.tenant_access_token')

if [ "$TENANT_TOKEN" == "null" ] || [ -z "$TENANT_TOKEN" ]; then
  echo "❌ 获取令牌失败: $(echo $TOKEN_RESPONSE | jq -r '.msg')"
  exit 1
fi

echo "✅ 获取令牌成功"

# -----------------------------------------------------------------------------
# 2. 配置事件订阅
# -----------------------------------------------------------------------------
echo ""
echo "📡 Step 2: 配置事件订阅..."

EVENTS=(
  "im.message.receive_v1"
  "im.message.created_v1"
  "im.message.updated_v1"
)

for event in "${EVENTS[@]}"; do
  curl -s -X POST "https://open.feishu.cn/open-apis/bot/v4/hook/" \
    -H "Authorization: Bearer ${TENANT_TOKEN}" \
    -H 'Content-Type: application/json' \
    -d "{
      \"url\": \"https://your-domain.com/webhook/${AGENT_ID}\",
      \"verification_token\": \"${VERIFICATION_TOKEN}\"
    }" > /dev/null
done

echo "✅ 事件订阅配置完成"

# -----------------------------------------------------------------------------
# 3. 生成配置文件
# -----------------------------------------------------------------------------
echo ""
echo "📡 Step 3: 生成配置文件..."

CONFIG_JSON=$(cat <<EOF
{
  "agent_id": "${AGENT_ID}",
  "feishu": {
    "app_id": "${APP_ID}",
    "app_secret": "${APP_SECRET}",
    "verification_token": "${VERIFICATION_TOKEN}",
    "enabled": true
  }
}
EOF
)

echo "$CONFIG_JSON" > "/Users/zhangyuhao/zhangyuhao/python/ai-learning-team/runtime/${AGENT_ID}_feishu.json"

echo "✅ 配置文件已生成: runtime/${AGENT_ID}_feishu.json"
echo ""
echo "🎉 ${AGENT_ID} 飞书机器人配置完成！"
SCRIPT

chmod +x /Users/zhangyuhao/zhangyuhao/python/ai-learning-team/scripts/feishu_config.sh

echo ""
echo "✅ 配置脚本已生成: scripts/feishu_config.sh"
echo ""
echo "============================================================================"
echo "📝 下一步操作"
echo "============================================================================"
echo ""
echo "1. 在飞书开放平台 (https://open.feishu.cn/) 创建应用"
echo "2. 添加上述权限列表"
echo "3. 获取 App ID、App Secret、Verification Token"
echo "4. 运行配置脚本："
echo ""
echo "   ./scripts/feishu_config.sh <AGENT_ID> <APP_ID> <APP_SECRET> <TOKEN>"
echo ""
echo "============================================================================"

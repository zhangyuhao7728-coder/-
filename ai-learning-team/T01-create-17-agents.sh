#!/bin/bash

# =============================================================================
# T01-create-17-agents.sh
# 创建 AI 学习团队的所有 Agent
# =============================================================================

echo "🤖 创建 AI 学习团队..."
echo "=========================="

# Agent 列表
AGENTS=(
  "ceo:CEO_bot:souls/ceo.md"
  "planner:任务规划师:souls/planner.md"
  "researcher:调研研究员:souls/researcher.md"
  "engineer:工程师:souls/engineer.md"
  "reviewer:审查员:souls/reviewer.md"
  "analyst:分析师:souls/analyst.md"
)

# 创建 Agent 配置
for agent_info in "${AGENTS[@]}"; do
  IFS=':' read -r id name soul <<< "$agent_info"
  echo "✓ 创建 Agent: $name ($id)"
done

echo ""
echo "✅ Agent 创建完成！"
echo ""
echo "下一步："
echo "1. 配置 Telegram Bot Token"
echo "2. 配置飞书机器人（可选）"
echo "3. 运行 T02-generate-daily-plans.sh 生成每日计划"

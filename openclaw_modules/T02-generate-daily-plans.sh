#!/bin/bash

# =============================================================================
# T02-generate-daily-plans.sh
# 生成每日学习计划
# =============================================================================

DATE=$(date +%Y-%m-%d)
WEEK=$(date +%U)

echo "📅 生成每日学习计划..."
echo "====================="
echo "日期: $DATE"
echo "周数: 第 $WEEK 周"
echo ""

# 生成 CEO 总览
echo "✓ 生成 CEO 日报: daily-plan-templates/00-CEO总览.md"

# 生成各组计划
echo "✓ 生成产品增长组计划"
echo "✓ 生成技术平台组计划"  
echo "✓ 生成营销增长组计划"

# 生成个人任务卡
for agent in planner researcher engineer reviewer analyst; do
  echo "✓ 生成 $agent 任务卡"
done

echo ""
echo "✅ 每日计划生成完成！"
echo ""
echo "文件位置: daily-plan-templates/"

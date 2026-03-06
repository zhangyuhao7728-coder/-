#!/bin/bash

# =============================================================================
# T03-setup-cron-jobs.sh
# 为 AI 学习团队配置定时任务
# =============================================================================

echo "⏰ 配置定时任务..."
echo "===================="

# 1. 每日 8:00 - 生成学习计划
echo "✓ 添加: 每日 8:00 生成学习计划"
# openclaw cron add \
#   --name "daily-plan-generator" \
#   --schedule "0 8 * * *" \
#   --task "运行 T02-generate-daily-plans.sh" \
#   --channel telegram \
#   --delivery announce

# 2. 每日 9:00 - 数据层执行
echo "✓ 添加: 每日 9:00 数据层执行"
# openclaw cron add \
#   --name "data-layer-morning" \
#   --schedule "0 9 * * *" \
#   --task "Analyst 昨日复盘 + Researcher 今日调研" \
#   --channel telegram \
#   --delivery announce

# 3. 每日 12:00 - 上午检查
echo "✓ 添加: 每日 12:00 上午检查"
# openclaw cron add \
#   --name "morning-progress-check" \
#   --schedule "0 12 * * *" \
#   --task "检查上午任务进度" \
#   --channel telegram \
#   --delivery announce

# 4. 每日 18:00 - 复盘总结
echo "✓ 添加: 每日 18:00 复盘总结"
# openclaw cron add \
#   --name "evening-review" \
#   --schedule "0 18 * * *" \
#   --task "CEO 复盘 + 明日计划" \
#   --channel telegram \
#   --delivery announce

# 5. 每周一 9:00 - 周计划
echo "✓ 添加: 每周一 9:00 周计划"
# openclaw cron add \
#   --name "weekly-plan-generator" \
#   --schedule "0 9 * * 1" \
#   --task "生成周计划" \
#   --channel telegram \
#   --delivery announce

# 6. 每周日 20:00 - 周复盘
echo "✓ 添加: 每周日 20:00 周复盘"
# openclaw cron add \
#   --name "weekly-review" \
#   --schedule "0 20 * * 0" \
#   --task "周报 + MEMORY 更新" \
#   --channel telegram \
#   --delivery announce

echo ""
echo "✅ 定时任务配置完成！"
echo ""
echo "当前定时任务:"
openclaw cron list

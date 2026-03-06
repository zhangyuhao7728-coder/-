#!/bin/bash
# daily_plan.sh - 每日学习计划生成
# 目标：大专AI技术应用专业 - 夯实基础 + 实战项目

cd ~/zhangyuhao/python/ai-learning-team

echo "📅 $(date '+%Y-%m-%d %H:%M:%S') - 开始生成每日计划"
echo "🎓 身份：大专AI技术应用专业学生"

# 1. 检查成本预算
python3 browser-system/cost_control.py check > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "❌ 成本预算检查失败"
    exit 1
fi

# 2. 获取星期几
WEEKDAY=$(date +%u)  # 1-7 (周一到周日)

# 3. 根据不同日期生成不同计划
case $WEEKDAY in
    1)  # 周一：Python基础
        echo "📚 周一：Python编程基础"
        PLAN="1. Python基础语法复习
2. 练习编写简单程序
3. 学习数据结构与算法入门"
        ;;
    2)  # 周二：数据分析
        echo "📊 周二：数据分析与可视化"
        PLAN="1. Pandas数据处理学习
2. Matplotlib可视化实践
3. 简单数据分析项目"
        ;;
    3)  # 周三：机器学习入门
        echo "🤖 周三：机器学习基础"
        PLAN="1. Scikit-learn入门
2. 监督学习算法原理
3. 简单分类任务实践"
        ;;
    4)  # 周四：深度学习
        echo "🧠 周四：深度学习基础"
        PLAN="1. 神经网络原理
2. TensorFlow/PyTorch入门
3. 手写数字识别项目"
        ;;
    5)  # 周五：AI应用
        echo "🚀 周五：AI应用实践"
        PLAN="1. 图像识别基础
2. 自然语言处理入门
3. 小项目实战"
        ;;
    6)  # 周六：综合项目
        echo "💻 周六：项目实战"
        PLAN="1. 综合项目开发
2. 代码优化与重构
3. Git版本控制"
        ;;
    7)  # 周日：复盘总结
        echo "📝 周日：复盘总结"
        PLAN="1. 本周知识回顾
2. 问题总结与解决
3. 下周计划制定"
        ;;
esac

# 4. 输出计划
echo ""
echo "==========================="
echo "📋 今日学习计划"
echo "==========================="
echo "$PLAN"
echo "==========================="

# 5. 备份昨日快照
if [ -f runtime/task_snapshot.json ]; then
    cp runtime/task_snapshot.json runtime/task_snapshot_backup.json
fi

# 6. 保存今日计划
echo "$PLAN" > runtime/today_plan.txt
echo "$(date '+%Y-%m-%d') - $PLAN" >> browser-system/logs/daily.log

echo "✅ 每日计划生成完成"

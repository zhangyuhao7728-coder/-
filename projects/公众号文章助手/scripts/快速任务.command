#!/bin/bash
cd ~/项目/Ai学习系统/projects/公众号文章助手

echo "╔════════════════════════════════╗"
echo "║     🚀 AI快速任务        ║"
echo "╚════════════════════════════════╝"
echo ""
echo "选择任务类型:"
echo "1. 写文章"
echo "2. 编程问题"
echo "3. 翻译"
echo "4. 总结内容"
echo "5. 自定义任务"
echo ""
read -p "请选择 (1-5): " choice

case $choice in
    1)
        task="写一篇公众号文章"
        ;;
    2)
        task="解答编程问题"
        ;;
    3)
        task="翻译内容"
        ;;
    4)
        task="总结内容"
        ;;
    5)
        echo "请输入任务:"
        read task
        ;;
    *)
        task="处理任务"
        ;;
esac

# 创建任务文件
TASK_FILE=tasks/$(date +%Y%m%d%H%M%S)_task.txt
echo "$task" > "$TASK_FILE"

echo ""
echo "✅ 任务已提交: $task"
echo "📁 位置: $TASK_FILE"

read -p "按回车键退出..."

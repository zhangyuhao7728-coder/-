#!/bin/bash
# 成本优化一键脚本

echo "========================================"
echo "💰 OpenClaw 成本优化"
echo "========================================"

# 1. 显示当前状态
echo ""
echo "📊 当前状态:"
echo "----------------------------------------"

# 模型
echo "当前模型: MiniMax-M2.5 (无限)"

# 检查Ollama
if pgrep -x "ollama" > /dev/null; then
    echo "Ollama: ✅ 运行中"
else
    echo "Ollama: ⏳ 未运行"
fi

# 2. 优化建议
echo ""
echo "💡 优化建议:"
echo "----------------------------------------"
echo "1. 使用本地Ollama模型代替API"
echo "2. 优化记忆系统减少token"
echo "3. 降低定时任务频率"
echo "4. 使用缓存减少重复请求"

# 3. 切换模型
echo ""
echo "🔄 快速切换:"
echo "----------------------------------------"
echo "• 切换到免费模型: openclaw models set qwen2.5:latest"
echo "• 切换到MiniMax: openclaw models set minimax-cn/MiniMax-M2.5"

# 4. 查看成本
echo ""
echo "📈 查看成本:"
echo "----------------------------------------"
echo "• 成本日志: ~/.openclaw/logs/cost.log"
echo "• 使用统计: ~/.openclaw/logs/cost_state.json"

echo ""
echo "========================================"

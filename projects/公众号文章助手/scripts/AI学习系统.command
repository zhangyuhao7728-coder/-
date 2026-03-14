#!/bin/bash
# AI学习系统主控面板

echo "========================================"
echo "🧠 AI学习系统 - 主控面板"
echo "========================================"

echo ""
echo "请选择功能："
echo ""
echo "1. 📝 选题系统 - 获取推荐主题"
echo "2. ✍️ 智能写作 - 生成文章"
echo "3. 📊 爆文分析 - 分析热门文章"
echo "4. 🔍 SEO优化 - 优化文章"
echo "5. 🎨 封面生成 - 生成文章封面"
echo "6. 📱 排版转换 - 转换为公众号格式"
echo "7. 📊 成本控制 - 查看/优化成本"
echo "8. 🔒 安全检查 - 系统安全状态"
echo "9. 📈 项目状态 - 查看所有状态"
echo ""
echo "0. 🚪 退出"
echo ""

read -p "请输入选项 (0-9): " choice

case $choice in
    1)
        echo "启动选题系统..."
        python3 crawler/选题系统.py
        ;;
    2)
        echo "启动智能写作..."
        python3 tools/智能写作V3.py
        ;;
    3)
        echo "启动爆文分析..."
        python3 crawler/爆文分析.py
        ;;
    4)
        echo "启动SEO优化..."
        python3 tools/文章优化.py
        ;;
    5)
        echo "启动封面生成..."
        python3 tools/生成封面.py
        ;;
    6)
        echo "启动排版转换..."
        echo "请输入要转换的文件路径："
        read filepath
        python3 formatter/markdown_to_wechat.py "$filepath"
        ;;
    7)
        echo "查看成本控制..."
        python3 tools/增强成本控制.py
        ;;
    8)
        echo "运行安全检查..."
        openclaw security audit
        ;;
    9)
        echo "查看项目状态..."
        echo "Gateway: $(openclaw gateway status | grep Listening)"
        echo "Cron: $(openclaw cron status | grep jobs)"
        echo "Skills: $(ls ~/.openclaw/skills/*.yaml 2>/dev/null | wc -l | tr -d ' ')个"
        ;;
    0)
        echo "再见！"
        exit 0
        ;;
    *)
        echo "无效选项"
        ;;
esac

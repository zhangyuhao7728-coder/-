#!/bin/bash

echo "========================================"
echo "WordPress AI 开发环境一键安装"
echo "========================================"

echo ""
echo "1. 检查Node.js..."
node -v || echo "请先安装Node.js"

echo ""
echo "2. 安装Claude Code..."
npm install -g @anthropic-ai/claude-code

echo ""
echo "3. 克隆官方技能..."
cd ~/项目/Ai学习系统
git clone https://github.com/WordPress/agent-skills.git

echo ""
echo "4. 安装技能..."
cd agent-skills
node shared/scripts/skillpack-build.mjs --clean
node shared/scripts/skillpack-install.mjs --global

echo ""
echo "========================================"
echo "✅ 安装完成！"
echo "========================================"
echo ""
echo "下一步："
echo "1. 下载WordPress Studio: https://developer.wordpress.com/studio/"
echo "2. 打开Studio，新建站点"
echo "3. 打开终端，输入: claude"
echo "4. 开始开发！"
echo ""

read -p "按回车键退出..."

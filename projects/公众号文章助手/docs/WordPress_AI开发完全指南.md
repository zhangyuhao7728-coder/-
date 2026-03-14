# WordPress AI 开发完全指南

## ✅ 已完成的配置

### 1. Claude Code ✅
```
npm install -g @anthropic-ai/claude-code
```

### 2. WordPress 官方技能包 ✅
- 已编译 ✅
- 已安装 13个技能 ✅

### 3. WordPress Studio
- 需要下载安装：https://developer.wordpress.com/studio/

---

## 🚀 快速开始

### 步骤1：打开WordPress Studio
1. 在Launchpad/Spotlight搜索 "WordPress Studio"
2. 打开应用

### 步骤2：创建站点
1. 点击 `+` 创建新站点
2. 输入站点名称
3. 等待创建完成

### 步骤3：开始开发
1. 点击站点
2. 选择「在Terminal中打开」
3. 输入 `claude`
4. 登录后描述需求开始开发

---

## 📋 可用技能 (13个)

| 技能 | 用途 |
|------|------|
| wp-plugin-development | 插件开发 |
| wp-block-development | 区块开发 |
| wp-block-themes | 主题开发 |
| wp-rest-api | REST API开发 |
| wp-phpstan | 代码质量分析 |
| wp-performance | 性能优化 |
| wordpress-router | 路由配置 |
| wp-wpcli-and-ops | 命令行运维 |
| wp-interactivity-api | 交互API |
| wp-abilities-api | 能力API |
| wp-project-triage | 项目诊断 |
| wp-playground | 在线测试 |
| wpds | 开发规范 |

---

## 💬 示例对话

### 创建插件
```
你说: 创建一个插件，在文章底部显示分享按钮

AI会:
- 创建插件结构
- 编写分享功能
- 告诉你在后台激活
```

### 添加设置页面
```
你说: 添加一个设置页面，可以自定义分享按钮的文字

AI会自动:
- 创建设置页面
- 添加菜单项
- 保存设置到数据库
```

---

## ⚠️ 注意事项

1. 需要先安装WordPress Studio
2. Claude Code需要登录账号
3. 所有操作在本地进行，很安全

---

## 📞 帮助

详细配置：configs/WordPress插件开发配置.json
教程文档：docs/WordPress插件开发指南.md

---

*配置完成: 2026-03-14*

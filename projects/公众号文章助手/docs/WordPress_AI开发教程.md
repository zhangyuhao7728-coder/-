# WordPress AI 开发教程

## 快速开始

### 1. 安装 Claude Code

```bash
# 方法1: npm安装
npm install @anthropic-ai/claude-code

# 方法2: 官网下载
# https://claude.ai/code
```

### 2. 安装 WordPress Studio

- macOS: App Store 或官网下载
- Windows: 官网下载
- 地址: https://developer.wordpress.com/studio/

### 3. 安装 WordPress 官方技能

```bash
git clone https://github.com/WordPress/agent-skills.git
cd agent-skills
node shared/scripts/skillpack-build.mjs --clean
node shared/scripts/skillpack-install.mjs --global
```

## 开发流程

1. 打开 WordPress Studio
2. 新建站点
3. 打开终端
4. 输入 `claude`
5. 描述你的需求

## 示例

```
我说: 我想要一个插件，能在后台显示"你好，名字"

AI会自动:
- 创建插件文件夹
- 生成标准结构文件
- 你去后台激活就能用
```

## 技巧

| 技巧 | 说明 |
|------|------|
| 说清位置 | 告诉AI你在哪个目录 |
| 描述具体 | 功能越具体越好 |
| 拆分需求 | 复杂功能分步说 |
| 让AI解释 | 不懂就问AI |

## 相关配置

- Claude Code配置: configs/claude_code配置.json
- WordPress Studio: configs/wordpress_studio配置.json
- 官方技能: ~/项目/Ai学习系统/agent-skills/

---

*更新: 2026-03-14*

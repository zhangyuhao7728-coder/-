# WordPress插件开发指南

## 完整工作流

### 第1步：安装Claude Code

```bash
# 方法1: npm安装
npm install -global @anthropic-ai/claude-code

# 方法2: 官网下载
# https://claude.ai/code
```

### 第2步：安装WordPress Studio

- 下载地址: https://developer.wordpress.com/studio/
- 支持 macOS 和 Windows

### 第3步：创建本地站点

1. 打开 WordPress Studio
2. 点击"新建站点"
3. 输入站点名称
4. 等待创建完成

### 第4步：启动开发

1. 在Studio中找到「在…中打开」→「Terminal」
2. 输入 `claude` 启动AI
3. 登录Claude账号
4. 开始描述你的需求

## 示例对话

### 示例1：创建简单插件

```
你说: 我想在WordPress后台顶部显示"你好，Nick"

AI会:
- 创建插件文件夹
- 生成主插件文件
- 告诉你在哪里激活
```

### 示例2：添加设置页面

```
你说: 给我加一个设置页面，可以修改显示的名字

AI会自动:
- 创建设置页面模板
- 添加菜单项
- 保存设置到数据库
```

## 常用提示词

| 功能 | 提示词 |
|------|--------|
| 创建插件 | "创建一个插件，功能是..." |
| 添加页面 | "添加一个设置页面" |
| 自定义文章 | "创建自定义文章类型" |
| 小工具 | "添加一个侧边栏小工具" |
| API接口 | "创建一个REST API接口" |

## 技能配置

位置: `configs/WordPress插件开发配置.json`

## 官方资源

- WordPress Studio: https://developer.wordpress.com/studio/
- 官方技能: https://github.com/WordPress/agent-skills

---

*更新: 2026-03-14*

# 使用 AI 开发 WordPress 的几个关键步骤！

**来源：** WordPress果酱  
**日期：** 2026年3月1日  
**作者：** WordPress果酱

---

## 文章总结

### 步骤1: 安装 WordPress Studio

- 官方免费本地开发工具
- 无需手动配置 PHP、MySQL、Docker 等环境
- 一键即可创建本地 WordPress 站点
- 支持 Windows、macOS 双平台
- 可快速创建、管理本地站点
- 还能与 WordPress.com/Pressable 同步
- 相比传统本地环境（XAMPP、LocalWP），零配置、轻量化、资源占用低

**地址：** https://developer.wordpress.com/studio/

---

### 步骤2: 安装 Claude Code

- AI编程工具
- 官网注册账号，选择付费套餐
- 从配置页下载官方安装包安装

**地址：** https://claude.ai/

**也可以通过npm安装：**
```bash
npm install @anthropic-ai/claude-code
```

---

### 步骤3: 开始写代码

1. 打开 WordPress Studio
2. 在"概览"标签里找到「在…中打开」
3. 点「Terminal」（终端）
4. 输入命令 `claude`
5. 登录 Claude 账号后即可开始描述需求开发

---

### 步骤4: 使用 WordPress 官方专业技能

- 安装 WordPress 官方提供的技能
- 教会 AI 正确地构建 WordPress
- 地址：https://github.com/WordPress/agent-skills

**13个专业技能包，包含：**
- WordPress开发最佳实践
- 官方开发规范
- 安全检查清单
- 可直接使用的脚本模板

**安装命令：**
```bash
git clone https://github.com/WordPress/agent-skills.git
cd agent-skills
node shared/scripts/skillpack-build.mjs --clean
node shared/scripts/skillpack-install.mjs --global
```

---

## 关键要点

1. WordPress Studio - 零配置本地开发
2. Claude Code - AI编程助手
3. 官方技能包 - 专业开发规范

---

*记录时间：2026-03-14*

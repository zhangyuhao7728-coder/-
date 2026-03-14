# 🛠️ AI公众号内容生产系统 V5

> 位于：`~/项目/Ai学习系统/projects/公众号文章助手/`

## 一、系统状态

| 组件 | 状态 | 说明 |
|------|------|------|
| Gateway | ✅ 运行中 | 127.0.0.1:18789 |
| 安全 | ✅ 0 critical | 无严重漏洞 |
| Cron任务 | ✅ 39个 | 正常运行 |
| Skills | ✅ 4个 | 已创建 |
| Ollama | ✅ 3个模型 | 本地免费 |

## 二、功能模块

### 1. 内容采集
- `crawler/选题系统.py` - 智能推荐主题
- `crawler/抓取文章.py` - 多平台采集
- `crawler/爆文分析.py` - 热门文章分析

### 2. 内容处理
- `tools/文章结构解析.py` - 提取文章结构
- `tools/风格分析.py` - 分析写作风格
- `tools/文章优化.py` - SEO优化

### 3. AI写作
- `tools/智能写作V3.py` - 基于学习技巧的写作
- `tools/风格生成.py` - 生成文章风格
- `tools/写作技巧库.py` - 写作技巧库

### 4. 排版发布
- `formatter/markdown_to_wechat.py` - 公众号格式
- `tools/生成封面.py` - 封面生成
- `tools/转手机版.py` - 手机版转换
- `cms.py` - 内容管理系统

### 5. 系统工具
- `tools/openclaw_cli.py` - CLI命令助手
- `tools/效率优化系统.py` - 7个效率方向
- `tools/增强成本控制.py` - 成本控制
- `tools/安全配置.py` - 安全配置
- `tools/security_check.py` - 安全检查

## 三、快速开始

```bash
cd ~/项目/Ai学习系统/projects/公众号文章助手

# 方式1: 使用主控面板
open AI学习系统.command

# 方式2: 命令行
python3 crawler/选题系统.py              # 获取选题
python3 tools/智能写作V3.py            # 生成文章
python3 tools/增强成本控制.py           # 成本控制
```

## 四、配置文件

| 文件 | 说明 |
|------|------|
| data/写作技巧库.json | 写作技巧 |
| data/效率优化配置.json | 7个方向 |
| data/成本控制配置.json | 成本设置 |
| data/多Agent配置.json | Agent配置 |
| data/记忆系统优化.json | 记忆优化 |

## 五、自定义Skills

| Skill | 功能 |
|-------|------|
| 每日简报 | 天气+日程+邮件+AI资讯 |
| 文章生成 | 公众号文章生成 |
| 数据分析 | 数据分析报告 |
| 安全检查 | 系统安全状态 |

## 六、成本

| 项目 | 费用 |
|------|------|
| 主模型 | MiniMax (无限) |
| 备用 | Ollama (免费) |
| 总成本 | **¥0** |

## 七、安全

- Gateway仅本地运行
- API Key放.env
- 定期安全审计
- 禁用危险功能

## 八、学习资源

- docs/效率提升10倍指南.md
- docs/项目升级完成报告.md
- data/公众号文章写作技巧学习.md

---
**版本**: V5 | **更新**: 2026-03-14

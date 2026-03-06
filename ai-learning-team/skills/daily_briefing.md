# 用例 52：每日简报生成器

## 概述

每天早上自动生成「今日简报」，整合天气 + 日历 + 新闻，一目了然。

## 技能依赖

- ✅ weather (已就绪)
- ⏳ gog (Google Calendar - 待安装)

## 已完成

- [x] 简报脚本：`scripts/daily_briefing.py`
- [x] 简报模板：`skills/daily_briefing.md`

## 待完成

- [ ] 天气 API（网络问题，wttr.in 无法访问）
- [ ] 日历集成（需要安装 gog 技能）
- [ ] Cron 任务设置

## 简报模板

```
📋 今日简报 - {{date}}

🌤️ 天气
- {{天气状况}}
- 温度：{{temp}}°C

📅 日程
- (需安装 gog)

📰 要闻
- (待配置)
```

## 下一步

1. 安装 gog 技能：`openclaw plugins install gog`
2. 配置 Google Calendar 权限
3. 设置 Cron：每天 6:30

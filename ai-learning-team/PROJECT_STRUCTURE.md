# AI学习系统 - 项目结构

## 目录结构

```
ai-learning-team/
├── scripts/          # Python脚本 (38个)
├── skills/          # Skill文档 (20个)
├── docs/            # 文档
├── config/          # 配置
└── memory/          # 记忆数据
```

## 脚本分类

### 1. 安全类 (8个)
| 脚本 | 功能 |
|------|------|
| ssh_key_scanner.py | SSH私钥扫描 |
| aws_credential_scanner.py | AWS凭证扫描 |
| git_history_cleaner.py | Git历史清理 |
| skill_supply_chain_audit.py | 技能供应链审计 |
| skill_preflight_checker.py | 技能安装预检 |
| keychain_access_tester.py | Keychain社工测试 |
| api_security_tester.py | API安全测试 |
| log_anomaly_detection.py | 日志异常检测 |

### 2. 运维类 (6个)
| 脚本 | 功能 |
|------|------|
| health_check.py | 健康检查 |
| auto_fix.py | 自动修复 |
| telegram_fix.py | Telegram修复 |
| gateway_keeper.py | Gateway保活 |
| token_optimizer.py | Token优化 |
| cron_dashboard.py | Cron看板 |

### 3. 学习类 (7个)
| 脚本 | 功能 |
|------|------|
| daily_briefing.py | 每日简报 |
| daily_journal.py | 学习日记 |
| daily_self_improvement.py | 自我提升 |
| morning_learning.py | 晨间学习 |
| rss_news_aggregator.py | RSS新闻聚合 |
| knowledge_graph.py | 知识图谱 |
| life_logger.py | 生活记忆 |

### 4. 系统类 (4个)
| 脚本 | 功能 |
|------|------|
| permissions.py | 权限管理 |
| infra_health_check.py | 基础设施检查 |
| heartbeat_monitor.py | 心跳监控 |
| nightly_tasks.py | 夜间任务 |

### 5. 其他 (13个)
- daily_plan.sh, feishu_setup.sh, l2_clean.py, l3_diff.py 等

## 技能 (Skills)

| 技能 | 功能 |
|------|------|
| daily_briefing.md | 每日简报 |
| daily_journal.md | 学习日记 |
| knowledge_graph.md | 知识图谱 |
| life_logger.md | 生活记忆 |
| permissions.md | 权限管理 |
| rss_news.md | RSS新闻 |
| weekly_archive.md | 周归档 |
| nightly_subagents.md | 夜间并行 |
| infra_health_check.md | 健康检查 |
| skill_preflight_checker.md | 技能预检 |
| heartbeat_monitor.md | 心跳监控 |

## Cron任务

| 任务 | 时间 | 状态 |
|------|------|------|
| rss-news-aggregator | 7:30 | ✅ |
| daily-journal | 21:00 | ✅ |
| health-check | 2小时 | ✅ |
| infra-health-check | 5:00 | ✅ |
| heartbeat-monitor | 30分钟 | ✅ |
| skill-security-check | 周日22:00 | ✅ |
| weekly-archive | 周日22:00 | ✅ |

## 安装统计

- 脚本: 38个
- 技能: 20个
- Cron: 15个

# 📁 OpenClaw AI学习系统 - 脚本分类说明

## 当前结构

```
openclaw_modules/scripts/
├── 01_安全类/          # 安全相关脚本
├── 02_运维类/          # 系统运维脚本
├── 03_学习类/          # 学习提升脚本
├── 04_自动化类/        # 自动任务脚本
└── 99_工具类/          # 通用工具
```

## 分类说明

### 01_安全类 (Security)
- ssh_key_scanner.py
- ssh_key_rotator.py
- aws_credential_scanner.py
- api_security_tester.py
- password_health_check.py
- 2fa_audit.py
- session_anomaly_detection.py
- keychain_access_tester.py
- log_anomaly_detection.py
- skill_supply_chain_audit.py
- github_stale_issue_cleanup.py
- github_issue_prioritizer.py

### 02_运维类 (Operations)
- health_check.py
- auto_fix.py
- telegram_fix.py
- gateway_keeper.py
- token_optimizer.py
- cron_dashboard.py
- openclaw_auto_maintenance.py
- openclaw_quick_fix.py
- infra_health_check.py
- heartbeat_monitor.py

### 03_学习类 (Learning)
- daily_briefing.py
- daily_journal.py
- daily_self_improvement.py
- morning_learning.py
- rss_news_aggregator.py
- knowledge_graph.py
- life_logger.py

### 04_自动化类 (Automation)
- nightly_tasks.py
- nightly_subagents.py
- auto_save.py
- confirm_push.py
- weekly_archive.py

### 99_工具类 (Tools)
- skill_preflight_checker.py
- skill_install_helper.py
- 2fa_improvement.py
- agent_latency_benchmark.py
- permissions.py
- gateway_keeper.py

## Cron任务分布

| 时间 | 任务 |
|------|------|
| 2:00 | agent-latency-benchmark |
| 5:00 | infra-health-check |
| 6:00 | daily-self-improvement |
| 7:00 | github-issue-prioritizer |
| 7:30 | rss-news-aggregator |
| 8:00 | token-optimizer |
| 21:00 | daily-journal |
| 22:00 | 知识图谱/日志/生活记录等 |
| 每周日 | 安全检查类 |

## 自动维护

- **每15分钟**: auto-fix
- **每30分钟**: heartbeat-monitor, telegram-fix
- **每小时**: auto-save-project
- **每4小时**: session-anomaly-check, openclaw-auto-maintenance
- **每天**: 各功能脚本

---
*更新时间: 2026-03-07*

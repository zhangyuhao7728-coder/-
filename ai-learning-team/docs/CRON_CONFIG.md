# AI 学习团队 - 定时任务配置

## 定时任务列表

### 1. 每日早上 8:00 - 生成学习计划
```bash
# 每天 8:00 自动生成当日学习计划
openclaw cron add \
  --name "daily-plan-generator" \
  --schedule "0 8 * * *" \
  --task "运行 T02-generate-daily-plans.sh 生成今日计划" \
  --channel telegram \
  --delivery announce
```

### 2. 每日早上 9:00 - 数据层先行
```bash
# 每天 9:00 执行数据层任务
# Analyst 分析昨日数据
# Researcher 调研今日内容
openclaw cron add \
  --name "data-layer-morning" \
  --schedule "0 9 * * *" \
  --task "执行数据层任务：analyst 昨日复盘 + researcher 今日调研" \
  --channel telegram \
  --delivery announce
```

### 3. 每日中午 12:00 - 上午进度检查
```bash
# 每天 12:00 检查上午任务完成情况
openclaw cron add \
  --name "morning-progress-check" \
  --schedule "0 12 * * *" \
  --task "检查上午任务进度，更新 task_snapshot.json" \
  --channel telegram \
  --delivery announce
```

### 4. 每日下午 18:00 - 复盘总结
```bash
# 每天 18:00 执行 CEO 复盘
openclaw cron add \
  --name "evening-review" \
  --schedule "0 18 * * *" \
  --task "执行 CEO 复盘：汇总成果 + 分析问题 + 制定明日计划" \
  --channel telegram \
  --delivery announce
```

### 5. 每周一 9:00 - 周计划生成
```bash
# 每周一生成周计划
openclaw cron add \
  --name "weekly-plan-generator" \
  --schedule "0 9 * * 1" \
  --task "生成周计划：L1 + L2 + L3 全套模板" \
  --channel telegram \
  --delivery announce
```

### 6. 每周日 20:00 - 周复盘
```bash
# 每周日生成周报
openclaw cron add \
  --name "weekly-review" \
  --schedule "0 20 * * 0" \
  --task "生成周报 + 更新 MEMORY.md 知识库" \
  --channel telegram \
  --delivery announce
```

---

## Cron 命令汇总

| 命令 | 说明 |
|------|------|
| `openclaw cron list` | 查看所有定时任务 |
| `openclaw cron add` | 添加新任务 |
| `openclaw cron disable <id>` | 禁用任务 |
| `openclaw cron enable <id>` | 启用任务 |
| `openclaw cron delete <id>` | 删除任务 |
| `openclaw cron run <id>` | 立即执行一次 |

---

## 时间线总览

```
08:00  生成每日计划 (T02脚本)
09:00  数据层执行 (Analyst + Researcher)
12:00  上午检查 (CEO Review)
18:00  复盘总结 (CEO Review + Analyst)
20:00  周复盘 (周日)
```

---

## 多 Agent 协作触发方式

### 方式 1: 通过 Skill 触发
```
skill: analyst_data_summary
  → 触发 → researcher_tech_lookup
  → 触发 → engineer_code_generator
```

### 方式 2: 通过 Agent 消息触发
```
CEO 消息 → planner → researcher → engineer → reviewer → analyst → CEO
```

### 方式 3: 通过 cron 事件触发
```
cron event → 读取 task_snapshot.json 
  → 判断状态 → 触发对应 Agent
```

---

## 注意事项

1. **频率控制**: 不要设太高，避免资源浪费
2. **状态检查**: 每次执行前检查 task_snapshot
3. **错误处理**: 失败自动升级到 CEO
4. **日志记录**: 所有执行记录到 decision_log

# =============================================================================
# Skill: Planner 任务拆解
# =============================================================================

## 基本信息
- **ID**: planner_squad_split
- **Name**: Task_Architect
- **Agent**: Planner (任务规划师)

## 职责
将 CEO 指令转化为 L2/L3 级的具体任务卡片

## 输入
| 字段 | 类型 | 说明 |
|------|------|------|
| milestone_goal | string | 里程碑目标 |
| agent_availability | array | Agent 可用状态 |

## 输出
| 字段 | 类型 | 说明 |
|------|------|------|
| task_cards | array | 任务卡片列表 |
| timeline_update | object | 时间线更新 |

## 模板
使用 `templates/daily/L3_TASK_CARD.md` 生成任务卡

## 触发条件
- new_goal_received: 新目标到达
- goal_updated: 目标更新

## 工作流程

### 1. 理解目标
- 分析 milestone_goal
- 识别关键需求点

### 2. 拆解任务
- 大任务拆 3-7 个子任务
- 每个任务分配具体 Agent
- 标注依赖关系

### 3. 生成任务卡
- 按 L3_TASK_CARD 模板生成
- 包含: 任务ID、描述、负责人、截止时间

### 4. 输出
```json
{
  "task_cards": [
    {
      "id": "task_001",
      "assignee": "researcher",
      "description": "调研 Python 爬虫技术",
      "deliverable": "调研报告",
      "deadline": "2026-03-02T10:00:00Z",
      "priority": "P1"
    }
  ],
  "timeline_update": {
    "start_time": "2026-03-02T09:00:00Z",
    "end_time": "2026-03-02T18:00:00Z"
  }
}
```

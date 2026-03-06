# TASK_OBJECT - 完整结构化模板

```json
{
  "task_id": "uuid-v4",
  "title": "任务标题",
  
  "mission_type": "QUERY | BUILD | DEBUG | RESEARCH",
  "complexity_level": "LOW | MEDIUM | HIGH | CRITICAL",
  
  "status": "CREATED | PLANNED | RESEARCHED | IMPLEMENTED | REVIEWED | REVIEW_FAILED | ANALYZED | ARCHIVED | ESCALATED | FAILED",
  "previous_status": null,
  "retry_control": {
    "retry_count": 0,
    "max_retry": 3,
    "retry_history": []
  },
  "max_retries": 3,
  
  "deliverable": "交付物描述",
  "success_metric": "可量化的成功标准",
  
  "state_flow": {
    "current": "CREATED",
    "history": ["CREATED"],
    "allowed_next": ["PLANNED"]
  },
  
  "risk_prediction": {
    "identified_risks": [
      {
        "risk_id": 1,
        "description": "风险描述",
        "likelihood": "LOW | MEDIUM | HIGH",
        "impact": "LOW | MEDIUM | HIGH",
        "mitigation": "缓解措施"
      }
    ],
    "overall_risk_level": "LOW | MEDIUM | HIGH"
  },
  
  "acceptance_criteria": [
    {
      "criterion": "验收标准描述",
      "passed": false,
      "evidence": "验证依据"
    }
  ],
  
  "rollback_mechanism": {
    "trigger": "REVIEWED = FAIL",
    "actions": [
      "状态回退至 IMPLEMENTED",
      "记录失败原因到 failure_log",
      "重新调度 engineer 修复",
      "retry_count + 1"
    ],
    "termination": "retry_count >= 3 → 标记 FAILED"
  },
  
  "failure_log": [],
  
  "subtasks": [
    {
      "id": "uuid",
      "assignee": "planner | researcher | engineer | reviewer | analyst",
      "description": "子任务描述",
      "status": "PENDING | IN_PROGRESS | COMPLETED | BLOCKED"
    }
  ],
  
  "gate_check": {
    "stage": "PLANNED | RESEARCHED | IMPLEMENTED | REVIEWED | ANALYZED",
    "passed": null,
    "severity": "low | medium | high | critical",
    "feedback": null,
    "checked_by": null,
    "checked_at": null
  },
  
  "review_result": {
    "severity": "low | medium | high | critical",
    "issues": [],
    "recommendation": null
  },
  
  "decision_log": [],
  
  "cooldown": {
    "last_decision_time": null,
    "min_interval_seconds": 5
  },
  
  "memory_system": {
    "memory_system": {
    "short_term_memory": {
      "task_context": [],
      "recent_actions": [],
      "active_constraints": [],
      "token_usage": 0,
      "max_tokens": 4000,
      "compression_strategy": "summarize | truncate | vectorize"
    },
    "long_term_memory": {
      "successful_patterns": [],
      "failure_patterns": [],
      "architecture_decisions": [],
      "optimization_strategies": [],
      "knowledge_index": [],
      "vector_store_enabled": false
    },
    "decision_memory": {
      "past_decisions": [],
      "decision_scores": [],
      "risk_outcomes": [],
      "reuse_threshold": 0.75
    },
    "memory_control": {
      "auto_cleanup": true,
      "cleanup_threshold": 0.85,
      "max_history_entries": 50,
      "last_cleanup_time": null
    },
    
    "locked": false,
    
    "context_control": {
      "core_context": {
        "required_fields": ["task_id", "title", "mission_type", "complexity_level"]
      },
      "task_snapshot": {
        "include_current_status": true,
        "include_review_result": true,
        "include_last_n_reviews": 1
      },
      "optional_history": {
        "include_last_n_logs": 0,
        "include_last_n_decisions": 0,
        "max_items": 3
      }
    }
  },
  
  "created_at": "ISO-8601",
  "updated_at": "ISO-8601",
  "completed_at": null
}
```

---

## 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| task_id | UUID | 唯一标识 |
| mission_type | Enum | 任务类型 |
| complexity_level | Enum | 复杂度等级 |
| status | Enum | 当前状态 |
| retry_count | Integer | 重试次数 |
| deliverable | String | 交付物 |
| success_metric | String | 成功标准 |
| risk_prediction | Object | 风险预测 |
| acceptance_criteria | Array | 验收标准列表 |
| rollback_mechanism | Object | 回退机制定义 |
| failure_log | Array | 失败记录 |
| subtasks | Array | 子任务列表 |
| gate_check | Object | 质量门控 |

---

## 状态流转图

```
┌─────────┐    PLANNED    ┌─────────┐   RESEARCHED   ┌───────────┐   IMPLEMENTED   ┌─────────┐
│ CREATED │ ───────────→ │ PLANNED │ ────────────→ │ RESEARCHED │ ───────────→ │IMPLEMENTED│
└─────────┘               └─────────┘                └───────────┘                 └─────────┘
                                                                                      ↓
                                                                                   REVIEWED
                                                                                      ↓
┌─────────┐    FAIL      ┌──────────┐ 修复后                             ┌─────────┐  ANALYZED
│  FAILED │ ←────────── │RETRY loop │ ──────────────────────────────────→│ ANALYZED│ ───→ ARCHIVED
└─────────┘  (≥3次)      └──────────┘                                    └─────────┘
```

---

## 复杂度与角色

| 复杂度 | 耗时 | 参与角色 |
|--------|------|----------|
| LOW | < 5min | engineer |
| MEDIUM | 5-30min | planner → engineer |
| HIGH | 30min-2h | planner → researcher → engineer |
| CRITICAL | > 2h | 全员协作 |

---

## 示例：构建计算器

```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Python 计算器程序",
  "mission_type": "BUILD",
  "complexity_level": "LOW",
  "status": "CREATED",
  "retry_count": 0,
  "deliverable": "可运行的 Python 计算器程序",
  "success_metric": "能正确执行加减乘除运算并输出结果",
  "risk_prediction": {
    "identified_risks": [],
    "overall_risk_level": "LOW"
  },
  "acceptance_criteria": [
    {"criterion": "程序可正常运行", "passed": false},
    {"criterion": "加减乘除运算正确", "passed": false},
    {"criterion": "除数为0时提示错误", "passed": false}
  ],
  "rollback_mechanism": {
    "trigger": "REVIEWED = FAIL",
    "actions": ["状态回退至 IMPLEMENTED", "记录失败原因", "重新调度 engineer"],
    "termination": "retry_count >= 3"
  }
}
```

# =============================================================================
# Skill: Reviewer 质量审计
# =============================================================================

## 基本信息
- **ID**: reviewer_quality_audit
- **Name**: Code_Guardian
- **Agent**: Reviewer (审查员)

## 职责
对 Engineer 输出的代码进行多维度安全性与性能审计

## 输入
| 字段 | 类型 | 说明 |
|------|------|------|
| code_snippet | string | 代码片段 |
| security_level | string | 安全级别 (normal/high) |

## 输出
| 字段 | 类型 | 说明 |
|------|------|------|
| audit_report | object | 审计报告 |
| fix_suggestions | array | 修复建议 |

## 审查维度
- syntax_check: 语法检查
- security_scan: 安全扫描
- performance_check: 性能检查
- readability_review: 可读性审查

## 触发条件
- review_requested: 收到审查请求

## 审查规则

### 1. 语法检查
- 运行 python -m py_compile
- 检查缩进
- 检查括号匹配

### 2. 安全扫描
- SQL 注入检测
- XSS 漏洞检测
- 密码明文检测

### 3. 性能检查
- 循环嵌套检测
- 数据库连接泄漏
- 内存使用

### 4. 可读性审查
- 变量命名
- 函数长度
- 注释充分性

## 输出格式
```json
{
  "audit_report": {
    "passed": true,
    "score": 85,
    "checks": {
      "syntax": "PASS",
      "security": "PASS",
      "performance": "WARN",
      "readability": "PASS"
    },
    "issues": [
      {
        "severity": "low",
        "line": 42,
        "message": "变量命名不够清晰",
        "suggestion": "将 'x' 改为 'user_count'"
      }
    ]
  },
  "fix_suggestions": [
    {
      "priority": 1,
      "description": "修复变量命名",
      "code_change": "x → user_count"
    }
  ]
}
```

## 判定规则
- **passed = true**: 无严重问题
- **severity = high**: 必须修复
- **severity = low**: 建议修复

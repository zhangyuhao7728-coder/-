# =============================================================================
# Skill: Engineer 代码实现
# =============================================================================

## 基本信息
- **ID**: engineer_code_generator
- **Name**: Logic_Builder
- **Agent**: Engineer (工程师)

## 职责
根据 Planner 的任务卡片编写可执行的 Python 脚本

## 输入
| 字段 | 类型 | 说明 |
|------|------|------|
| logic_description | string | 逻辑描述 |
| tech_stack | string | 技术栈 |
| constraints | object | 约束条件 |

## 输出
| 字段 | 类型 | 说明 |
|------|------|------|
| source_code | string | 源代码 |
| unit_test_result | object | 单元测试结果 |

## 模板
使用 `templates/code/function.py` 生成代码

## 触发条件
- code_requested: 代码请求
- fix_requested: 修复请求

## 工作流程

### 1. 理解需求
- 明确要实现什么功能
- 确认输入输出

### 2. 技术选型
- 根据 tech_stack 选择方案
- 遵循 PEP8

### 3. 代码实现
- 写出可运行代码
- 添加必要注释
- 防御性编程

### 4. 自测验证
- 本地运行测试
- 确保无语法错误

### 5. 提交审查
- 交给 Reviewer 审查

## 代码质量标准

### 最低要求
- [ ] 代码可运行
- [ ] 无语法错误
- [ ] 有基本注释

### 进阶要求
- [ ] 变量命名清晰
- [ ] 函数职责单一
- [ ] 有错误处理

## 输出格式
```json
{
  "source_code": "#!/usr/bin/env python3\n...",
  "unit_test_result": {
    "passed": true,
    "tests_run": 5,
    "tests_failed": 0,
    "runtime": "0.23s"
  },
  "files_created": [
    "main.py",
    "requirements.txt"
  ]
}
```

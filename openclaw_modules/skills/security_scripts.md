# 安全类脚本完整列表

## 已安装 (9个)

### 1. SSH相关
| 脚本 | 功能 | Cron |
|------|------|------|
| ssh_key_scanner.py | SSH私钥扫描 | 每周日 |
| ssh_key_rotator.py | SSH密钥自动轮换 | 需要配置 |

### 2. 云服务安全
| 脚本 | 功能 | Cron |
|------|------|------|
| aws_credential_scanner.py | AWS凭证扫描 | 每周一 |
| api_security_tester.py | API安全测试 | 每周六 |

### 3. 系统安全
| 脚本 | 功能 | Cron |
|------|------|------|
| password_health_check.py | 密码健康检查 | 每周日 |
| 2fa_audit.py | 双因素认证审计 | 每周一 |
| session_anomaly_detection.py | 会话异常检测 | 每4小时 |
| keychain_access_tester.py | Keychain社工测试 | 每周五 |

### 4. 日志/审计
| 脚本 | 功能 | Cron |
|------|------|------|
| log_anomaly_detection.py | 日志异常检测 | 每天23:00 |
| skill_supply_chain_audit.py | 技能供应链审计 | 每周三 |

### 5. 基础设施
| 脚本 | 功能 | Cron |
|------|------|------|
| health_check.py | 健康检查 | 每2小时 |
| infra_health_check.py | 基础设施检查 | 每天5:00 |

## 测试结果

| 脚本 | 状态 |
|------|------|
| ssh_key_scanner | ✅ 发现46个问题 |
| password_health_check | ✅ 通过 |
| 2fa_audit | ⚠️ 1/4覆盖 |
| session_anomaly_detection | ✅ 无异常 |

## 安全建议

1. 开启更多2FA服务
2. 定期轮换SSH密钥
3. 监控异常会话
4. 保持日志审计

# 第四类：安全类技能

## 用例05：SSH密钥自动轮换

### 功能
- 定期自动更换SSH密钥
- 90天自动轮换
- 备份旧密钥

### 命令
```bash
python scripts/ssh_key_rotator.py
```

### Cron
- ⏰ 每周日检查

---

## 用例06：密码健康检查

### 功能
- 检查系统密码策略
- 检查Keychain
- 密码强度评估

### 命令
```bash
python scripts/password_health_check.py
```

### Cron
- ⏰ 每周日22:00

---

## 用例07：双因素认证审计

### 功能
- 检查Apple ID 2FA
- 检查Google Chrome 2FA
- 检查GitHub 2FA
- 检查Touch ID

### 命令
```bash
python scripts/2fa_audit.py
```

### Cron
- ⏰ 每周一22:00

---

## 用例08：会话异常检测

### 功能
- 检查SSH会话
- 检测异常登录
- 监控会话数量

### 命令
```bash
python scripts/session_anomaly_detection.py
```

### Cron
- ⏰ 每4小时

---

## 已安装安全技能

| 用例 | 名称 | 状态 |
|------|------|------|
| 05 | SSH密钥自动轮换 | ✅ |
| 06 | 密码健康检查 | ✅ |
| 07 | 2FA审计 | ✅ |
| 08 | 会话异常检测 | ✅ |
| 09 | SSH私钥扫描 | ✅ 已安装 |
| 19 | 日志异常检测 | ✅ 已安装 |
| 30 | Keychain社工测试 | ✅ 已安装 |
| 31 | 技能供应链审计 | ✅ 已安装 |

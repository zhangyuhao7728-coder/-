#!/usr/bin/env python3
"""
Security Monitor - 安全监控中心
功能：
1. Gateway状态监控
2. 异常登录检测
3. 异常命令检测
4. Token扫描
5. 系统负载监控
6. 自动报警
"""
import os
import time
import subprocess
import requests
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor

# 导入各安全模块
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from security.audit_logger_enhanced import get_logger as get_audit_logger
except:
    get_audit_logger = None

try:
    from security.token_guard_enhanced import get_guard as get_token_guard
except:
    get_token_guard = None

try:
    from security.health_guard_enhanced import get_guard as get_health_guard
except:
    get_health_guard = None


class SecurityMonitor:
    """安全监控中心"""
    
    # 监控配置
    CONFIG = {
        'check_interval': 60,        # 检查间隔(秒)
        'alert_interval': 300,       # 报警间隔(秒)
        'max_retries': 3,            # 最大重试
    }
    
    def __init__(self):
        """初始化"""
        self.running = False
        self.stats = {
            'checks': 0,
            'alerts': 0,
            'issues': 0,
            'resolved': 0
        }
        
        self.alerts: List[dict] = []
        self.last_alert_time = {}
        
        # 初始化子模块
        self._init_modules()
    
    def _init_modules(self):
        """初始化子模块"""
        self.audit_logger = get_audit_logger() if get_audit_logger else None
        self.token_guard = get_token_guard() if get_token_guard else None
        self.health_guard = get_health_guard() if get_health_guard else None
    
    # ========== Gateway 监控 ==========
    
    def check_gateway(self) -> dict:
        """检查 Gateway 状态"""
        try:
            resp = requests.get('http://localhost:18789/health', timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                if data.get('ok') and data.get('status') == 'live':
                    return {'healthy': True, 'status': 'running'}
            
            return {'healthy': False, 'status': 'error', 'message': data}
        except Exception as e:
            return {'healthy': False, 'status': 'down', 'message': str(e)}
    
    # ========== 登录监控 ==========
    
    def check_failed_logins(self, minutes: int = 10) -> List[dict]:
        """检查异常登录"""
        if not self.audit_logger:
            return []
        
        # 查询最近的登录
        logs = self.audit_logger.query(
            operation='login',
            limit=100
        )
        
        failed = []
        threshold = datetime.now() - timedelta(minutes=minutes)
        
        for log in logs:
            log_time = datetime.fromisoformat(log['timestamp'])
            if log_time > threshold and log.get('status') == 'FAILED':
                failed.append(log)
        
        return failed
    
    # ========== 命令监控 ==========
    
    def check_suspicious_commands(self, minutes: int = 10) -> List[dict]:
        """检查异常命令"""
        if not self.audit_logger:
            return []
        
        logs = self.audit_logger.query(
            operation='command',
            limit=100
        )
        
        suspicious = []
        threshold = datetime.now() - timedelta(minutes=minutes)
        
        # 危险命令关键词
        dangerous_keywords = ['sudo', 'rm -rf', 'curl', 'wget', 'chmod 777']
        
        for log in logs:
            log_time = datetime.fromisoformat(log['timestamp'])
            if log_time > threshold:
                command = log.get('command', '')
                if any(kw in command.lower() for kw in dangerous_keywords):
                    suspicious.append(log)
        
        return suspicious
    
    # ========== Token 扫描 ==========
    
    def scan_tokens(self) -> dict:
        """扫描Token泄漏"""
        if not self.token_guard:
            return {'scanned': 0, 'issues': 0}
        
        results = self.token_guard.scan_project()
        
        total = sum(len(v) for v in results.values())
        
        return {
            'scanned': self.token_guard.stats.get('files_scanned', 0),
            'issues': total,
            'details': results
        }
    
    # ========== 系统负载 ==========
    
    def check_system_load(self) -> dict:
        """检查系统负载"""
        try:
            # CPU
            result = subprocess.run(
                ['ps', 'aux'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            lines = result.stdout.strip().split('\n')
            
            # 计算平均CPU
            cpu_sum = 0
            mem_sum = 0
            process_count = 0
            
            for line in lines[1:]:
                parts = line.split()
                if len(parts) >= 3:
                    try:
                        cpu_sum += float(parts[2])
                        mem_sum += float(parts[3])
                        process_count += 1
                    except:
                        pass
            
            avg_cpu = cpu_sum / process_count if process_count else 0
            avg_mem = mem_sum / process_count if process_count else 0
            
            # 磁盘
            disk_result = subprocess.run(
                ['df', '-h', '/'],
                capture_output=True,
                text=True
            )
            
            disk_usage = disk_result.stdout.strip().split('\n')[1].split()[4] if disk_result.stdout else 'N/A'
            
            return {
                'cpu': f"{avg_cpu:.1f}%",
                'memory': f"{avg_mem:.1f}%",
                'disk': disk_usage,
                'processes': process_count,
                'healthy': avg_cpu < 80 and avg_mem < 80
            }
        except Exception as e:
            return {'healthy': False, 'error': str(e)}
    
    # ========== 综合检查 ==========
    
    def run_health_check(self) -> dict:
        """运行健康检查"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'gateway': self.check_gateway(),
            'system': self.check_system_load(),
        }
        
        return results
    
    def run_security_check(self) -> dict:
        """运行安全检查"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'failed_logins': self.check_failed_logins(),
            'suspicious_commands': self.check_suspicious_commands(),
            'token_scan': self.scan_tokens(),
        }
        
        return results
    
    def run_full_check(self) -> dict:
        """运行完整检查"""
        self.stats['checks'] += 1
        
        health = self.run_health_check()
        security = self.run_security_check()
        
        # 汇总
        issues = []
        
        # Gateway 问题
        if not health['gateway']['healthy']:
            issues.append({
                'type': 'gateway',
                'severity': 'critical',
                'message': health['gateway'].get('message', 'Gateway down')
            })
        
        # 系统问题
        if not health['system'].get('healthy', True):
            issues.append({
                'type': 'system',
                'severity': 'warning',
                'message': f"High load: {health['system'].get('cpu')}"
            })
        
        # 登录问题
        if security['failed_logins']:
            issues.append({
                'type': 'login',
                'severity': 'warning',
                'message': f"{len(security['failed_logins'])} failed logins"
            })
        
        # 命令问题
        if security['suspicious_commands']:
            issues.append({
                'type': 'command',
                'severity': 'warning',
                'message': f"{len(security['suspicious_commands'])} suspicious commands"
            })
        
        # Token 问题
        if security['token_scan'].get('issues', 0) > 0:
            issues.append({
                'type': 'token',
                'severity': 'critical',
                'message': f"{security['token_scan']['issues']} tokens leaked"
            })
        
        self.stats['issues'] = len(issues)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'healthy': len(issues) == 0,
            'issues': issues,
            'health': health,
            'security': security,
            'stats': self.stats.copy()
        }
    
    # ========== 报警 ==========
    
    def should_alert(self, alert_type: str) -> bool:
        """检查是否应该报警"""
        now = time.time()
        
        if alert_type not in self.last_alert_time:
            return True
        
        return now - self.last_alert_time[alert_type] > self.CONFIG['alert_interval']
    
    def send_alert(self, alert_type: str, message: str, severity: str = 'warning'):
        """发送报警"""
        if not self.should_alert(alert_type):
            return
        
        self.last_alert_time[alert_type] = time.time()
        self.stats['alerts'] += 1
        
        alert = {
            'timestamp': datetime.now().isoformat(),
            'type': alert_type,
            'severity': severity,
            'message': message
        }
        
        self.alerts.append(alert)
        
        # 打印报警
        icon = '🔴' if severity == 'critical' else '🟡'
        print(f"{icon} 报警 [{alert_type}]: {message}")
        
        # TODO: 发送 Telegram
    
    # ========== 主循环 ==========
    
    def start_monitoring(self, interval: int = None):
        """开始监控"""
        interval = interval or self.CONFIG['check_interval']
        self.running = True
        
        print(f"🛡️ 安全监控启动 (间隔: {interval}秒)")
        
        while self.running:
            try:
                # 运行检查
                result = self.run_full_check()
                
                # 检查问题并报警
                for issue in result['issues']:
                    self.send_alert(
                        issue['type'],
                        issue['message'],
                        issue['severity']
                    )
                
                if result['healthy']:
                    print(f"✅ 健康检查通过")
                else:
                    print(f"⚠️ 发现 {len(result['issues'])} 个问题")
                
            except Exception as e:
                print(f"❌ 监控错误: {e}")
            
            time.sleep(interval)
    
    def stop_monitoring(self):
        """停止监控"""
        self.running = False
        print("🛡️ 安全监控已停止")
    
    # ========== 查询 ==========
    
    def get_alerts(self, limit: int = 50) -> List[dict]:
        return self.alerts[-limit:]
    
    def get_stats(self) -> dict:
        return self.stats.copy()


# 全局实例
_monitor = None

def get_monitor() -> SecurityMonitor:
    global _monitor
    if _monitor is None:
        _monitor = SecurityMonitor()
    return _monitor

def run_security_check() -> dict:
    return get_monitor().run_full_check()

def get_security_status() -> dict:
    monitor = get_monitor()
    return {
        'health': monitor.run_health_check(),
        'security': monitor.run_security_check(),
        'stats': monitor.get_stats()
    }


# 测试
if __name__ == "__main__":
    monitor = get_monitor()
    
    print("=== Security Monitor 测试 ===\n")
    
    # 完整检查
    print("运行完整检查...")
    result = run_security_check()
    
    print(f"\n健康状态: {'✅ 正常' if result['healthy'] else '⚠️ 异常'}")
    print(f"发现问题: {len(result['issues'])}")
    
    for issue in result['issues']:
        print(f"  - [{issue['severity']}] {issue['type']}: {issue['message']}")
    
    print(f"\n统计: {result['stats']}")

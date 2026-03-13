#!/usr/bin/env python3
"""
Enhanced Health Guard - 增强版健康守卫
功能：
1. Gateway 检测
2. Ollama 检测
3. MiniMax API 检测
4. 自动重启
5. 自动报警
"""
import os
import time
import subprocess
import requests
from typing import Dict, List, Optional
from datetime import datetime


class EnhancedHealthGuard:
    """增强版健康守卫"""
    
    # 服务配置
    SERVICES = {
        'gateway': {
            'name': 'OpenClaw Gateway',
            'url': 'http://localhost:18789/health',
            'process': 'openclaw.*gateway',
            'restart_cmd': ['openclaw', 'gateway', 'restart'],
            'critical': True
        },
        'ollama': {
            'name': 'Ollama',
            'url': 'http://localhost:11434/api/tags',
            'process': 'ollama',
            'restart_cmd': ['brew', 'services', 'restart', 'ollama'],
            'critical': False
        },
        'minimax': {
            'name': 'MiniMax API',
            'url': 'https://api.minimax.io/v1/models',
            'api_key_required': True,
            'critical': False
        },
    }
    
    def __init__(self):
        """初始化"""
        self.stats = {
            'checks': 0,
            'healthy': 0,
            'unhealthy': 0,
            'restarts': 0
        }
        
        self.alerts: List[dict] = []
        self.log: List[dict] = []
    
    def _log(self, event: str, service: str = None, details: dict = None):
        """记录日志"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'event': event,
            'service': service,
            'details': details or {}
        }
        self.log.append(entry)
        
        # 写入文件
        log_file = os.path.expanduser('~/.openclaw/logs/health_guard.log')
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        with open(log_file, 'a') as f:
            f.write(f"{entry['timestamp']} {event}: {service} {details}\n")
    
    # ========== 检测方法 ==========
    
    def check_gateway(self) -> dict:
        """检查 Gateway"""
        service = self.SERVICES['gateway']
        
        try:
            # 检查 HTTP
            resp = requests.get(service['url'], timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                if data.get('ok') and data.get('status') == 'live':
                    return {
                        'healthy': True,
                        'status': 'running',
                        'message': 'Gateway is healthy'
                    }
        except Exception as e:
            pass
        
        # 检查进程
        try:
            result = subprocess.run(
                ['pgrep', '-f', service['process']],
                capture_output=True,
                timeout=5
            )
            if result.returncode == 0:
                return {
                    'healthy': False,
                    'status': 'not_responding',
                    'message': 'Process running but not responding'
                }
        except:
            pass
        
        return {
            'healthy': False,
            'status': 'down',
            'message': 'Gateway is down'
        }
    
    def check_ollama(self) -> dict:
        """检查 Ollama"""
        service = self.SERVICES['ollama']
        
        try:
            resp = requests.get(service['url'], timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                models = data.get('models', [])
                return {
                    'healthy': True,
                    'status': 'running',
                    'message': f'Ollama is healthy ({len(models)} models)'
                }
        except Exception as e:
            pass
        
        return {
            'healthy': False,
            'status': 'down',
            'message': 'Ollama is not running'
        }
    
    def check_minimax(self) -> dict:
        """检查 MiniMax API"""
        service = self.SERVICES['minimax']
        
        # 需要 API Key
        api_key = os.environ.get('MINIMAX_API_KEY', '')
        if not api_key:
            return {
                'healthy': False,
                'status': 'no_api_key',
                'message': 'MINIMAX_API_KEY not set'
            }
        
        try:
            headers = {'Authorization': f'Bearer {api_key}'}
            resp = requests.get(service['url'], headers=headers, timeout=10)
            
            if resp.status_code == 200:
                return {
                    'healthy': True,
                    'status': 'running',
                    'message': 'MiniMax API is healthy'
                }
            elif resp.status_code == 401:
                return {
                    'healthy': False,
                    'status': 'invalid_key',
                    'message': 'API key is invalid'
                }
            else:
                return {
                    'healthy': False,
                    'status': 'error',
                    'message': f'HTTP {resp.status_code}'
                }
        except requests.exceptions.Timeout:
            return {
                'healthy': False,
                'status': 'timeout',
                'message': 'Request timeout'
            }
        except Exception as e:
            return {
                'healthy': False,
                'status': 'error',
                'message': str(e)
            }
    
    def check_service(self, name: str) -> dict:
        """检查服务"""
        if name == 'gateway':
            return self.check_gateway()
        elif name == 'ollama':
            return self.check_ollama()
        elif name == 'minimax':
            return self.check_minimax()
        else:
            return {'healthy': False, 'status': 'unknown'}
    
    # ========== 重启方法 ==========
    
    def restart_gateway(self) -> bool:
        """重启 Gateway"""
        try:
            self._log('restart_attempt', 'gateway')
            
            # 停止
            subprocess.run(['openclaw', 'gateway', 'stop'], 
                        capture_output=True, timeout=15)
            time.sleep(2)
            
            # 启动
            result = subprocess.run(['openclaw', 'gateway', 'start'],
                               capture_output=True, timeout=30)
            
            if result.returncode == 0:
                time.sleep(3)
                
                # 验证
                if self.check_gateway()['healthy']:
                    self.stats['restarts'] += 1
                    self._log('restart_success', 'gateway')
                    return True
            
            self._log('restart_failed', 'gateway', {'error': result.stderr.decode()})
            return False
            
        except Exception as e:
            self._log('restart_error', 'gateway', {'error': str(e)})
            return False
    
    def restart_ollama(self) -> bool:
        """重启 Ollama"""
        try:
            subprocess.run(['brew', 'services', 'restart', 'ollama'],
                        capture_output=True, timeout=30)
            time.sleep(5)
            
            if self.check_ollama()['healthy']:
                self.stats['restarts'] += 1
                self._log('restart_success', 'ollama')
                return True
            
            return False
        except Exception as e:
            self._log('restart_error', 'ollama', {'error': str(e)})
            return False
    
    def restart_service(self, name: str) -> bool:
        """重启服务"""
        if name == 'gateway':
            return self.restart_gateway()
        elif name == 'ollama':
            return self.restart_ollama()
        return False
    
    # ========== 报警方法 ==========
    
    def send_alert(self, service: str, status: dict):
        """发送报警"""
        alert = {
            'timestamp': datetime.now().isoformat(),
            'service': service,
            'status': status['status'],
            'message': status['message']
        }
        self.alerts.append(alert)
        
        self._log('alert', service, status)
        
        # TODO: 发送 Telegram 消息
        print(f"🚨 报警: {service} - {status['message']}")
    
    # ========== 主检查 ==========
    
    def check_all(self, auto_restart: bool = True, alert_on_failure: bool = True) -> dict:
        """
        检查所有服务
        
        Args:
            auto_restart: 是否自动重启
            alert_on_failure: 是否报警
        """
        self.stats['checks'] += 1
        
        results = {}
        all_healthy = True
        
        for name, config in self.SERVICES.items():
            # 检查
            result = self.check_service(name)
            results[name] = result
            
            if result['healthy']:
                self.stats['healthy'] += 1
            else:
                self.stats['unhealthy'] += 1
                all_healthy = False
                
                # 自动重启
                if auto_restart and config.get('critical', False):
                    success = self.restart_service(name)
                    if success:
                        results[name] = self.check_service(name)
                        if results[name]['healthy']:
                            all_healthy = True
                
                # 报警
                if alert_on_failure:
                    self.send_alert(name, result)
        
        return {
            'healthy': all_healthy,
            'services': results,
            'stats': self.stats.copy()
        }
    
    def get_status(self) -> dict:
        """获取状态"""
        results = {}
        
        for name in self.SERVICES.keys():
            results[name] = self.check_service(name)
        
        return {
            'services': results,
            'stats': self.stats.copy()
        }
    
    def get_stats(self) -> dict:
        return self.stats.copy()
    
    def get_alerts(self, limit: int = 10) -> List[dict]:
        return self.alerts[-limit:]


# 全局实例
_guard = None

def get_guard() -> EnhancedHealthGuard:
    global _guard
    if _guard is None:
        _guard = EnhancedHealthGuard()
    return _guard

def health_check() -> dict:
    return get_guard().check_all()

def get_health_status() -> dict:
    return get_guard().get_status()


# 测试
if __name__ == "__main__":
    guard = get_guard()
    
    print("=== Enhanced Health Guard 测试 ===\n")
    
    # 获取状态
    print("服务状态:")
    status = guard.get_status()
    
    for name, result in status['services'].items():
        icon = "✅" if result['healthy'] else "❌"
        print(f"  {icon} {name}: {result['message']}")
    
    # 检查全部
    print("\n完整检查:")
    result = guard.check_all(auto_restart=False)
    print(f"  整体: {'✅ 健康' if result['healthy'] else '❌ 异常'}")
    print(f"  统计: {result['stats']}")

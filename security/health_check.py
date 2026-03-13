#!/usr/bin/env python3
"""
Health Check Module - 健康检查模块
功能：
1. Gateway 健康检查
2. Ollama 健康检查
3. 服务状态
"""
import os
import requests
import subprocess
from typing import Dict
from datetime import datetime


class HealthChecker:
    """健康检查器"""
    
    def __init__(self):
        self.services = {
            'gateway': {
                'name': 'OpenClaw Gateway',
                'url': 'http://localhost:18789/health',
                'critical': True
            },
            'ollama': {
                'name': 'Ollama',
                'url': 'http://localhost:11434/api/tags',
                'critical': False
            }
        }
    
    def check_gateway(self) -> Dict:
        """检查 Gateway"""
        try:
            resp = requests.get(self.services['gateway']['url'], timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                if data.get('ok') and data.get('status') == 'live':
                    return {
                        'healthy': True,
                        'name': 'Gateway',
                        'status': 'running'
                    }
            return {
                'healthy': False,
                'name': 'Gateway',
                'status': 'error',
                'message': str(resp.text)
            }
        except Exception as e:
            return {
                'healthy': False,
                'name': 'Gateway',
                'status': 'down',
                'message': str(e)
            }
    
    def check_ollama(self) -> Dict:
        """检查 Ollama"""
        try:
            resp = requests.get(self.services['ollama']['url'], timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                models = data.get('models', [])
                return {
                    'healthy': True,
                    'name': 'Ollama',
                    'status': 'running',
                    'models': len(models)
                }
            return {
                'healthy': False,
                'name': 'Ollama',
                'status': 'error'
            }
        except Exception as e:
            return {
                'healthy': False,
                'name': 'Ollama',
                'status': 'down',
                'message': str(e)
            }
    
    def check_all(self) -> Dict:
        """检查所有服务"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'services': {
                'gateway': self.check_gateway(),
                'ollama': self.check_ollama()
            }
        }
        
        # 汇总
        healthy = all(s.get('healthy', False) for s in results['services'].values())
        results['healthy'] = healthy
        
        return results


# 全局实例
_checker = None

def get_health_checker() -> HealthChecker:
    global _checker
    if _checker is None:
        _checker = HealthChecker()
    return _checker

def health_check() -> Dict:
    return get_health_checker().check_all()


# 测试
if __name__ == "__main__":
    print("=== Health Check 测试 ===\n")
    
    result = health_check()
    
    print(f"整体状态: {'✅ 健康' if result['healthy'] else '❌ 异常'}\n")
    
    for name, info in result['services'].items():
        icon = "✅" if info['healthy'] else "❌"
        msg = info.get('message', info.get('status', ''))
        print(f"{icon} {info['name']}: {msg}")

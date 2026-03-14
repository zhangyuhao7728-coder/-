#!/usr/bin/env python3
"""
智能安全防御系统 V2
自动化验证、拒绝危险、自我升级
"""
import re
import json
import os
from datetime import datetime
from typing import Dict, List

class IntelligentSecuritySystem:
    """智能安全防御系统"""
    
    def __init__(self):
        self.db_dir = os.path.expanduser("~/.openclaw/security")
        os.makedirs(self.db_dir, exist_ok=True)
        
        self.threat_db = f"{self.db_dir}/threat_db.json"
        self.log_file = f"{self.db_dir}/security_log.json"
        self.trusted_db = f"{self.db_dir}/trusted_sources.json"
        
        self.load_databases()
    
    def load_databases(self):
        """加载数据库"""
        # 威胁数据库
        if os.path.exists(self.threat_db):
            with open(self.threat_db, 'r', encoding='utf-8') as f:
                self.threats = json.load(f)
        else:
            self.threats = self.get_default_threats()
            self.save_threats()
        
        # 可信来源
        if os.path.exists(self.trusted_db):
            with open(self.trusted_db, 'r', encoding='utf-8') as f:
                self.trusted = json.load(f)
        else:
            self.trusted = self.get_default_trusted()
            self.save_trusted()
    
    def get_default_threats(self) -> dict:
        """默认威胁模式"""
        return {
            'patterns': {
                'system_commands': [
                    r'rm\s+-rf',
                    r'dd\s+if=',
                    r'format\s+',
                    r'mkfs',
                    r'chmod\s+777',
                    r'chown\s+',
                ],
                'shell_injection': [
                    r';\s*rm\s',
                    r'&&\s*rm\s',
                    r'\|\s*rm\s',
                    r';\s*curl\s',
                    r';\s*wget\s',
                ],
                'download_execute': [
                    r'curl\s+.*\|',
                    r'wget\s+.*\|',
                    r'python\s+-m\s+http',
                    r'powershell\s+-enc',
                ],
                'credential_access': [
                    r'password\s*=\s*["\']',
                    r'api[_-]?key\s*=\s*["\']',
                    r'secret\s*=\s*["\']',
                    r'token\s*=\s*["\']',
                ],
                'network': [
                    r'nc\s+-e',
                    r'/dev/tcp/',
                    r'bash\s+-i',
                ]
            },
            'suspicious_domains': [
                '.tk', '.ml', '.ga', '.cf', '.gq',
                'malware', 'virus', 'trojan', 'hack'
            ],
            'phishing': [
                r'点击此处.*登录',
                r'请输入.*密码',
                r'验证.*账户',
                r'紧急.*通知'
            ]
        }
    
    def get_default_trusted(self) -> dict:
        """默认可信来源"""
        return {
            'domains': [
                'mp.weixin.qq.com',
                'zhihu.com',
                'juejin.cn',
                'csdn.net',
                'github.com',
                'baidu.com',
                '36kr.com',
                'huxiu.com'
            ],
            'sources': [
                '开发者阿橙',
                '极客公园',
                '36kr',
                '虎嗅',
                '公众号'
            ]
        }
    
    def save_threats(self):
        with open(self.threat_db, 'w', encoding='utf-8') as f:
            json.dump(self.threats, f, ensure_ascii=False, indent=2)
    
    def save_trusted(self):
        with open(self.trusted_db, 'w', encoding='utf-8') as f:
            json.dump(self.trusted, f, ensure_ascii=False, indent=2)
    
    # ========== 验证方法 ==========
    def validate_url(self, url: str) -> dict:
        """验证URL"""
        result = {
            'safe': True,
            'trusted': False,
            'risk': 'none',
            'details': []
        }
        
        # 提取域名
        domain_match = re.search(r'https?://([^/]+)', url)
        if not domain_match:
            result['safe'] = False
            result['risk'] = 'unknown'
            result['details'].append('无法解析域名')
            return result
        
        domain = domain_match.group(1).lower()
        
        # 检查可信域名
        for trusted in self.trusted['domains']:
            if trusted in domain:
                result['trusted'] = True
                result['details'].append(f'可信域名: {trusted}')
                break
        
        # 检查危险域名
        for suspicious in self.threats['suspicious_domains']:
            if suspicious in domain:
                result['safe'] = False
                result['risk'] = 'high'
                result['details'].append(f'可疑域名: {suspicious}')
        
        return result
    
    def validate_content(self, content: str) -> dict:
        """验证内容"""
        result = {
            'safe': True,
            'risk': 'none',
            'threats_found': []
        }
        
        # 检查所有危险模式
        for category, patterns in self.threats['patterns'].items():
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    result['safe'] = False
                    result['risk'] = 'high'
                    result['threats_found'].append({
                        'category': category,
                        'pattern': pattern
                    })
        
        # 检查钓鱼
        for phishing in self.threats['phishing']:
            if re.search(phishing, content):
                result['safe'] = False
                result['risk'] = 'medium'
                result['threats_found'].append({
                    'category': 'phishing',
                    'pattern': phishing
                })
        
        return result
    
    def validate_all(self, url: str = None, content: str = None, source: str = None) -> dict:
        """综合验证"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'overall_safe': True,
            'action': 'allow',
            'checks': {}
        }
        
        # URL检查
        if url:
            url_result = self.validate_url(url)
            report['checks']['url'] = url_result
            if not url_result['safe']:
                report['overall_safe'] = False
                report['action'] = 'block'
        
        # 内容检查
        if content:
            content_result = self.validate_content(content)
            report['checks']['content'] = content_result
            if not content_result['safe']:
                report['overall_safe'] = False
                report['action'] = 'block'
        
        # 来源检查
        if source:
            source_result = self.validate_source(source)
            report['checks']['source'] = source_result
        
        # 记录日志
        self.log_event(report)
        
        return report
    
    def validate_source(self, source: str) -> dict:
        """验证来源"""
        result = {'trusted': False, 'source_type': 'unknown'}
        
        for trusted in self.trusted['sources']:
            if trusted in source:
                result['trusted'] = True
                result['source_type'] = 'trusted'
                break
        
        if '微信' in source or '公众号' in source:
            result['trusted'] = True
            result['source_type'] = 'wechat'
        
        return result
    
    def log_event(self, report: dict):
        """记录安全事件"""
        logs = []
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        
        logs.append(report)
        
        # 只保留最近100条
        logs = logs[-100:]
        
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
    
    # ========== 自我升级 ==========
    def add_trusted_source(self, source: str):
        """添加可信来源"""
        if source not in self.trusted['domains']:
            self.trusted['domains'].append(source)
            self.save_trusted()
            return True
        return False
    
    def add_threat_pattern(self, pattern: str, category: str = 'custom'):
        """添加威胁模式"""
        if 'custom' not in self.threats['patterns']:
            self.threats['patterns']['custom'] = []
        
        if pattern not in self.threats['patterns']['custom']:
            self.threats['patterns']['custom'].append(pattern)
            self.save_threats()
            return True
        return False
    
    def auto_update(self):
        """自我升级 - 自动更新威胁库"""
        # 这里可以添加从外部获取最新威胁信息的逻辑
        # 目前是基础版本
        return {
            'status': 'updated',
            'threat_count': sum(len(p) for p in self.threats['patterns'].values()),
            'trusted_count': len(self.trusted['domains'])
        }
    
    # ========== 快速检查 ==========
    def is_safe(self, url: str = None, content: str = None) -> bool:
        """快速判断是否安全"""
        report = self.validate_all(url=url, content=content)
        return report['overall_safe']
    
    def get_action(self, url: str = None, content: str = None) -> str:
        """获取动作"""
        report = self.validate_all(url=url, content=content)
        return report['action']

# 命令行工具
def main():
    import sys
    
    validator = IntelligentSecuritySystem()
    
    print("="*50)
    print("🛡️ 智能安全防御系统 V2")
    print("="*50)
    
    # 显示状态
    status = validator.auto_update()
    print(f"\n📊 系统状态:")
    print(f"   威胁模式: {status['threat_count']}")
    print(f"   可信来源: {status['trusted_count']}")
    
    # 测试URL
    test_url = "https://mp.weixin.qq.com/s/test"
    result = validator.validate_url(test_url)
    print(f"\n🧪 测试URL: {test_url}")
    print(f"   安全: {'✅' if result['safe'] else '❌'}")
    print(f"   可信: {'✅' if result['trusted'] else '❌'}")

if __name__ == '__main__':
    main()


# ========== 集成警报系统 ==========
def alert_and_block(url: str = None, content: str = None):
    """检测到威胁时自动警报并拦截"""
    from tools.安全警报系统 import alert_on_threat
    
    result = validate_all(url, content)
    
    if not result['overall_safe']:
        # 发送警报
        if url:
            alert_on_threat('suspicious_url', f'可疑URL: {url}', 'high')
        if content:
            alert_on_threat('dangerous_command', f'危险内容检测: {content[:50]}', 'high')
        
        return {
            'action': 'block',
            'reason': '安全威胁已拦截',
            'alert_sent': True
        }
    
    return {
        'action': 'allow',
        'reason': '安全验证通过',
        'alert_sent': False
    }

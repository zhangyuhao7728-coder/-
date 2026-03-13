#!/usr/bin/env python3
"""
Enhanced Network Guard - 增强版网络守卫
功能：
1. 允许/禁止域名
2. API端点限制
3. 本地服务白名单
4. 出站流量监控
"""
import os
import re
import socket
from typing import Dict, List, Set, Tuple, Optional


class EnhancedNetworkGuard:
    """增强版网络守卫"""
    
    # ========== 允许的域名 ==========
    ALLOWED_DOMAINS = {
        # AI API
        'api.minimax.io',
        'api.minimax.chat',
        'api.minimax.com',
        'api.openai.com',
        'api.anthropic.com',
        'api.cohere.ai',
        
        # 火山引擎
        'ark.cn-beijing.volces.com',
        'ark.cn-shanghai.volces.com',
        'ark.cn-guangzhou.volces.com',
        
        # Telegram
        'api.telegram.org',
        'telegram.org',
        
        # 爬虫测试网站
        'quotes.toscrape.com',
        'news.163.com',
        'news.sina.com.cn',
        'reddit.com',
        'www.reddit.com',
        
        # 本地
        'localhost',
        '127.0.0.1',
        '0.0.0.0',
        
        # 常用
        'github.com',
        'api.github.com',
        'pypi.org',
        'pypi.python.org',
        'npmjs.org',
    }
    
    # ========== 允许的IP ==========
    ALLOWED_IPS = {
        '127.0.0.1',
        'localhost',
        '0.0.0.0',
        '::1',
    }
    
    # ========== 允许的端口 ==========
    ALLOWED_PORTS = {
        80, 443,          # HTTP/HTTPS
        18789,            # OpenClaw Gateway
        11434,            # Ollama
        3000, 3001,      # 开发服务器
        5000, 5173,      # 前端开发
        8000, 8080,      # Python/Node服务
    }
    
    # ========== 禁止的域名 ==========
    FORBIDDEN_DOMAINS = {
        # 恶意网站 (示例)
        'evil.com',
        'malware.com',
        'phishing.com',
    }
    
    # ========== 允许的协议 ==========
    ALLOWED_PROTOCOLS = {
        'http',
        'https',
    }
    
    def __init__(self):
        """初始化"""
        # 编译域名模式
        self._allowed_patterns = [
            re.compile(self._domain_to_pattern(domain))
            for domain in self.ALLOWED_DOMAINS
        ]
        
        # 统计
        self.stats = {
            'total_checks': 0,
            'allowed': 0,
            'denied': 0
        }
        
        # 日志
        self.log: List[dict] = []
    
    def _domain_to_pattern(self, domain: str) -> str:
        """域名转正则"""
        # 转换 *.example.com 为 .*\.example\.com$
        pattern = domain.replace('.', r'\\.')
        return f'.*{pattern}$'
    
    def _log(self, action: str, target: str, result: str):
        """记录日志"""
        from datetime import datetime
        entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'target': target,
            'result': result
        }
        self.log.append(entry)
        
        # 保存到文件
        log_file = os.path.expanduser('~/.openclaw/logs/network_guard.log')
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        with open(log_file, 'a') as f:
            f.write(f"{entry['timestamp']} {action}: {target} -> {result}\n")
    
    def _is_ip(self, target: str) -> bool:
        """检查是否是IP"""
        try:
            socket.inet_aton(target)
            return True
        except:
            return False
    
    def _resolve_domain(self, domain: str) -> List[str]:
        """解析域名"""
        try:
            ips = socket.getaddrinfo(domain, None)
            return list(set(info[4][0] for info in ips))
        except:
            return []
    
    def _check_domain(self, domain: str) -> Tuple[bool, str]:
        """检查域名"""
        domain = domain.lower().strip()
        
        # 直接匹配
        if domain in self.ALLOWED_DOMAINS:
            return True, ''
        
        # 模式匹配
        for pattern in self._allowed_patterns:
            if pattern.match(domain):
                return True, ''
        
        # 子域名检查
        for allowed in self.ALLOWED_DOMAINS:
            if domain.endswith('.' + allowed):
                return True, ''
        
        return False, f'域名不在白名单: {domain}'
    
    def _check_ip(self, ip: str) -> Tuple[bool, str]:
        """检查IP"""
        if ip in self.ALLOWED_IPS:
            return True, ''
        
        # 检查是否是本地IP
        if ip.startswith('127.') or ip.startswith('10.') or ip.startswith('192.168.'):
            return True, ''
        
        return False, f'IP不在白名单: {ip}'
    
    def _check_port(self, port: int) -> Tuple[bool, str]:
        """检查端口"""
        if port in self.ALLOWED_PORTS:
            return True, ''
        
        return False, f'端口不在白名单: {port}'
    
    def _check_protocol(self, protocol: str) -> Tuple[bool, str]:
        """检查协议"""
        if protocol.lower() in self.ALLOWED_PROTOCOLS:
            return True, ''
        
        return False, f'协议不允许: {protocol}'
    
    def validate_url(self, url: str) -> dict:
        """
        验证URL
        
        Returns:
            dict: {
                'allowed': bool,
                'reason': str,
                'domain': str,
                'ip': str,
                'port': int,
                'protocol': str
            }
        """
        self.stats['total_checks'] += 1
        
        # 解析URL
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
        except:
            self.stats['denied'] += 1
            self._log('validate_url', url, 'invalid_url')
            return {
                'allowed': False,
                'reason': '无效的URL格式',
                'url': url
            }
        
        protocol = parsed.scheme
        domain = parsed.hostname or ''
        port = parsed.port or (443 if protocol == 'https' else 80)
        
        # 1. 检查协议
        allowed, reason = self._check_protocol(protocol)
        if not allowed:
            self.stats['denied'] += 1
            self._log('validate_url', url, 'protocol_denied')
            return {
                'allowed': False,
                'reason': reason,
                'protocol': protocol
            }
        
        # 2. 检查域名
        allowed, reason = self._check_domain(domain)
        if not allowed:
            self.stats['denied'] += 1
            self._log('validate_url', url, 'domain_denied')
            return {
                'allowed': False,
                'reason': reason,
                'domain': domain
            }
        
        # 3. 检查端口
        allowed, reason = self._check_port(port)
        if not allowed:
            self.stats['denied'] += 1
            self._log('validate_url', url, 'port_denied')
            return {
                'allowed': False,
                'reason': reason,
                'port': port
            }
        
        # 通过
        self.stats['allowed'] += 1
        self._log('validate_url', url, 'allowed')
        
        return {
            'allowed': True,
            'reason': '验证通过',
            'domain': domain,
            'port': port,
            'protocol': protocol
        }
    
    def validate_domain(self, domain: str) -> dict:
        """验证域名"""
        self.stats['total_checks'] += 1
        
        allowed, reason = self._check_domain(domain)
        
        if allowed:
            self.stats['allowed'] += 1
            self._log('validate_domain', domain, 'allowed')
            return {'allowed': True, 'reason': '域名允许'}
        
        self.stats['denied'] += 1
        self._log('validate_domain', domain, 'denied')
        return {'allowed': False, 'reason': reason}
    
    def check(self, url: str) -> bool:
        """检查URL，如果不允许则抛异常"""
        result = self.validate_url(url)
        
        if not result['allowed']:
            raise PermissionError(
                f"🚫 网络访问被阻止\n"
                f"URL: {url}\n"
                f"原因: {result['reason']}"
            )
        
        return True
    
    # ========== 配置管理 ==========
    
    def add_allowed_domain(self, domain: str):
        """添加允许的域名"""
        self.ALLOWED_DOMAINS.add(domain)
        # 重新编译模式
        self._allowed_patterns = [
            re.compile(self._domain_to_pattern(d))
            for d in self.ALLOWED_DOMAINS
        ]
    
    def add_allowed_ip(self, ip: str):
        """添加允许的IP"""
        self.ALLOWED_IPS.add(ip)
    
    def add_allowed_port(self, port: int):
        """添加允许的端口"""
        self.ALLOWED_PORTS.add(port)
    
    def remove_allowed_domain(self, domain: str):
        """移除允许的域名"""
        self.ALLOWED_DOMAINS.discard(domain)
    
    def get_allowed_domains(self) -> Set[str]:
        """获取允许的域名"""
        return self.ALLOWED_DOMAINS.copy()
    
    def get_stats(self) -> Dict:
        return self.stats.copy()
    
    def get_log(self, limit: int = 100) -> List[dict]:
        return self.log[-limit:]


# 全局实例
_guard = None

def get_guard() -> EnhancedNetworkGuard:
    global _guard
    if _guard is None:
        _guard = EnhancedNetworkGuard()
    return _guard

def validate_url(url: str) -> dict:
    return get_guard().validate_url(url)

def check_url(url: str) -> bool:
    return get_guard().check(url)


# 测试
if __name__ == "__main__":
    guard = get_guard()
    
    print("=== Enhanced Network Guard 测试 ===\n")
    
    # 测试URL
    tests = [
        # 允许
        "https://api.minimax.io/v1/chat",
        "https://api.telegram.org/bot123:getMe",
        "http://quotes.toscrape.com/",
        "https://ark.cn-beijing.volces.com/api/v3/",
        "http://localhost:18789/health",
        
        # 禁止
        "https://evil.com/malware",
        "https://google.com/search",
    ]
    
    print(f"{'URL':<50} {'结果':<12}")
    print("-" * 65)
    
    for url in tests:
        result = guard.validate_url(url)
        status = "✅" if result['allowed'] else "❌"
        print(f"{url[:47]:<50} {result['allowed']:<12} {status}")
    
    print(f"\n统计: {guard.get_stats()}")

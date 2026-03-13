#!/usr/bin/env python3
"""
Enhanced Token Guard - 增强版密钥守卫
功能：
1. 扫描代码中的密钥
2. 检测敏感信息泄漏
3. 自动报警
4. 密钥格式验证
"""
import os
import re
import hashlib
from typing import Dict, List, Tuple, Optional
from datetime import datetime


class EnhancedTokenGuard:
    """增强版密钥守卫"""
    
    # ========== 密钥模式 ==========
    TOKEN_PATTERNS = {
        # OpenAI
        'openai': [
            r'sk-[a-zA-Z0-9]{20,}',
            r'OPENAI_API_KEY\s*[=:]\s*["\']?[a-zA-Z0-9-]{20,}',
        ],
        
        # Anthropic/Claude
        'anthropic': [
            r'sk-ant-[a-zA-Z0-9_-]{20,}',
            r'ANTHROPIC_API_KEY\s*[=:]\s*["\']?[a-zA-Z0-9-]{20,}',
        ],
        
        # MiniMax
        'minimax': [
            r'sk-cp-[a-zA-Z0-9_-]{20,}',
            r'MINIMAX_API_KEY\s*[=:]\s*["\']?[a-zA-Z0-9-]{20,}',
        ],
        
        # Volcengine
        'volcengine': [
            r'[a-z0-9]{32,}',  # Volcengine keys are typically 32+ hex chars
            r'VOLCENGINE_API_KEY\s*[=:]\s*["\']?[a-zA-Z0-9-]{20,}',
        ],
        
        # GitHub
        'github': [
            r'ghp_[a-zA-Z0-9]{36,}',
            r'github_pat_[a-zA-Z0-9_]{22,}',
            r'GITHUB_TOKEN\s*[=:]\s*["\']?[a-zA-Z0-9_-]{20,}',
        ],
        
        # Telegram
        'telegram': [
            r'\d{8,10}:[a-zA-Z0-9_-]{35,}',
            r'TELEGRAM_BOT_TOKEN\s*[=:]\s*["\']?[\d:]{10,35}',
        ],
        
        # AWS
        'aws': [
            r'AKIA[0-9A-Z]{16}',
            r'AWS_ACCESS_KEY_ID\s*[=:]\s*["\']?AKIA[0-9A-Z]{16}',
            r'aws_secret_access_key\s*[=:]\s*["\']?[a-zA-Z0-9/+=]{40}',
        ],
        
        # JWT
        'jwt': [
            r'eyJ[a-zA-Z0-9_-]*\.eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*',
        ],
        
        # Generic
        'generic': [
            r'api[_-]?key\s*[=:]\s*["\']?[a-zA-Z0-9_-]{16,}',
            r'secret[_-]?key\s*[=:]\s*["\']?[a-zA-Z0-9_-]{16,}',
            r'access[_-]?token\s*[=:]\s*["\']?[a-zA-Z0-9_-]{16,}',
            r'auth[_-]?token\s*[=:]\s*["\']?[a-zA-Z0-9_-]{16,}',
            r'password\s*[=:]\s*["\'][^"\']{6,}',
        ],
    }
    
    # ========== 禁止的文件 ==========
    FORBIDDEN_FILES = [
        '.env',
        '.env.local',
        '.env.production',
        'credentials',
        'secrets.json',
        'tokens.json',
    ]
    
    # ========== 允许的目录 ==========
    ALLOWED_SCAN_DIRS = [
        os.path.expanduser('~/项目/Ai学习系统'),
    ]
    
    def __init__(self):
        """初始化"""
        # 编译正则表达式
        self._compiled_patterns = {}
        for token_type, patterns in self.TOKEN_PATTERNS.items():
            self._compiled_patterns[token_type] = [
                re.compile(p, re.IGNORECASE) for p in patterns
            ]
        
        # 统计
        self.stats = {
            'files_scanned': 0,
            'tokens_found': 0,
            'alerts': 0
        }
        
        # 告警日志
        self.alerts: List[dict] = []
        
        # 已知的密钥哈希（用于过滤误报）
        self.known_tokens: set = set()
    
    def _hash_token(self, token: str) -> str:
        """哈希密钥"""
        return hashlib.sha256(token.encode()).hexdigest()[:16]
    
    def add_known_token(self, token: str):
        """添加已知密钥"""
        self.known_tokens.add(self._hash_token(token))
    
    def _log_alert(self, token_type: str, file_path: str, line_num: int, line_content: str):
        """记录告警"""
        # 隐藏密钥
        hidden = re.sub(r'[a-zA-Z0-9_-]{8,}', '***', line_content[:50])
        
        alert = {
            'timestamp': datetime.now().isoformat(),
            'type': token_type,
            'file': file_path,
            'line': line_num,
            'preview': hidden
        }
        
        self.alerts.append(alert)
        self.stats['alerts'] += 1
        
        # 保存到文件
        log_file = os.path.expanduser('~/.openclaw/logs/token_alerts.log')
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        with open(log_file, 'a') as f:
            f.write(f"{alert['timestamp']} [{token_type}] {file_path}:{line_num} - {hidden}\n")
    
    def _scan_line(self, line: str) -> List[Tuple[str, str]]:
        """扫描单行"""
        found = []
        
        for token_type, patterns in self._compiled_patterns.items():
            for pattern in patterns:
                match = pattern.search(line)
                if match:
                    token = match.group(0)
                    # 检查是否已知
                    if self._hash_token(token) not in self.known_tokens:
                        found.append((token_type, token))
        
        return found
    
    def scan_file(self, file_path: str) -> List[dict]:
        """扫描单个文件"""
        results = []
        
        # 检查是否是禁止的文件
        filename = os.path.basename(file_path)
        if filename in self.FORBIDDEN_FILES:
            # 记录但不完全阻止
            results.append({
                'type': 'sensitive_file',
                'file': file_path,
                'line': 0,
                'message': f'敏感文件: {filename}'
            })
        
        # 扫描内容
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    matches = self._scan_line(line)
                    
                    for token_type, token in matches:
                        # 记录告警
                        self._log_alert(token_type, file_path, line_num, line)
                        
                        results.append({
                            'type': token_type,
                            'file': file_path,
                            'line': line_num,
                            'token_preview': token[:10] + '...'
                        })
                        
                        self.stats['tokens_found'] += 1
        except Exception as e:
            pass
        
        return results
    
    def scan_directory(self, directory: str, extensions: List[str] = None) -> List[dict]:
        """扫描目录"""
        results = []
        
        if extensions is None:
            extensions = ['.py', '.js', '.ts', '.json', '.yaml', '.yml', '.sh', '.env', '.txt']
        
        directory = os.path.abspath(directory)
        
        for root, dirs, files in os.walk(directory):
            # 跳过特定目录
            dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', 'venv', '.venv']]
            
            for file in files:
                # 检查扩展名
                if not any(file.endswith(ext) for ext in extensions):
                    continue
                
                file_path = os.path.join(root, file)
                self.stats['files_scanned'] += 1
                
                # 扫描
                file_results = self.scan_file(file_path)
                results.extend(file_results)
        
        return results
    
    def scan_project(self) -> Dict:
        """扫描整个项目"""
        results = {}
        
        for scan_dir in self.ALLOWED_SCAN_DIRS:
            if os.path.exists(scan_dir):
                results[scan_dir] = self.scan_directory(scan_dir)
        
        return results
    
    def check_string(self, text: str) -> List[dict]:
        """检查字符串是否包含密钥"""
        results = []
        
        matches = self._scan_line(text)
        
        for token_type, token in matches:
            if self._hash_token(token) not in self.known_tokens:
                results.append({
                    'type': token_type,
                    'token_preview': token[:10] + '...'
                })
        
        return results
    
    def get_alerts(self, limit: int = 100) -> List[dict]:
        """获取告警列表"""
        return self.alerts[-limit:]
    
    def get_stats(self) -> Dict:
        return self.stats.copy()
    
    def clear_alerts(self):
        """清除告警"""
        self.alerts = []


# 全局实例
_guard = None

def get_guard() -> EnhancedTokenGuard:
    global _guard
    if _guard is None:
        _guard = EnhancedTokenGuard()
    return _guard

def scan_file(file_path: str) -> List[dict]:
    return get_guard().scan_file(file_path)

def scan_directory(directory: str) -> List[dict]:
    return get_guard().scan_directory(directory)

def check_string(text: str) -> List[dict]:
    return get_guard().check_string(text)


# 测试
if __name__ == "__main__":
    guard = get_guard()
    
    print("=== Enhanced Token Guard 测试 ===\n")
    
    # 测试字符串
    test_strings = [
        "OPENAI_API_KEY=sk-abc123456789",
        "TELEGRAM_TOKEN=123456789:ABCdefGHIjklMNOpqrSTUvwxYZ",
        "MINIMAX_API_KEY=sk-cp-abc123",
        "github_token=ghp_abcdefghijklmnopqrstuvwxyz1234567890",
        "normal_text = 'hello world'",
    ]
    
    print("字符串检测:")
    for text in test_strings:
        results = guard.check_string(text)
        if results:
            print(f"  ⚠️ 发现: {results[0]['type']} - {text[:40]}")
        else:
            print(f"  ✅ 安全: {text[:40]}")
    
    print(f"\n统计: {guard.get_stats()}")
    
    print("\n=== 扫描项目 ===")
    results = guard.scan_project()
    total = sum(len(v) for v in results.values())
    print(f"扫描完成: {total} 个问题")

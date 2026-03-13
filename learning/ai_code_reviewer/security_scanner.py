#!/usr/bin/env python3
"""
Security Scanner - 安全扫描
"""
import re
from typing import Dict, List


class SecurityScanner:
    """安全扫描"""
    
    # 危险模式
    DANGEROUS_PATTERNS = [
        (r'eval\s*\(', "eval()可能导致代码注入"),
        (r'exec\s*\(', "exec()可能导致代码注入"),
        (r'__import__\s*\(', "动态导入可能有风险"),
        (r'pickle\.loads?', "pickle反序列化可能有风险"),
        (r'subprocess\.call.*shell=True', "shell=True可能有注入风险"),
        (r'os\.system', "os.system可能有注入风险"),
        (r'os\.popen', "os.popen可能有注入风险"),
        (r'sql.*\+', "SQL拼接可能有注入风险"),
        (r'password\s*=\s*["\']', "避免硬编码密码"),
        (r'api[_-]?key\s*=\s*["\']', "避免硬编码API密钥"),
    ]
    
    def scan(self, code: str) -> Dict:
        """扫描安全问题"""
        
        issues = []
        
        for pattern, desc in self.DANGEROUS_PATTERNS:
            if re.search(pattern, code, re.IGNORECASE):
                issues.append({
                    "type": "security",
                    "pattern": pattern,
                    "description": desc
                })
        
        return {
            "safe": len(issues) == 0,
            "issues": issues if issues else [{"type": "safe", "description": "未发现安全问题"}],
            "risk_level": self._get_risk(issues)
        }
    
    def _get_risk(self, issues: List) -> str:
        if not issues:
            return "低"
        if len(issues) <= 2:
            return "中"
        return "高"


_scanner = None

def get_security_scanner():
    global _scanner
    if _scanner is None:
        _scanner = SecurityScanner()
    return _scanner

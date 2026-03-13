#!/usr/bin/env python3
"""
Token Scanner Module - Token扫描模块
功能：
1. 扫描项目中的Token
2. 分类统计
3. 生成报告
"""
import os
import re
from typing import Dict, List
from datetime import datetime


class TokenScanner:
    """Token扫描器"""
    
    # Token模式
    PATTERNS = {
        'telegram': r'\d{8,10}:[a-zA-Z0-9_-]{35,}',
        'openai': r'sk-[a-zA-Z0-9]{20,}',
        'minimax': r'sk-cp-[a-zA-Z0-9_-]{20,}',
        'github': r'ghp_[a-zA-Z0-9]{36,}',
        'anthropic': r'sk-ant-[a-zA-Z0-9_-]{20,}',
    }
    
    def __init__(self):
        """初始化"""
        self.results = []
    
    def scan_file(self, filepath: str) -> List[dict]:
        """扫描文件"""
        findings = []
        
        try:
            with open(filepath, 'r', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    for token_type, pattern in self.PATTERNS.items():
                        matches = re.finditer(pattern, line)
                        for match in matches:
                            findings.append({
                                'file': filepath,
                                'line': line_num,
                                'type': token_type,
                                'preview': line.strip()[:50],
                                'timestamp': datetime.now().isoformat()
                            })
        except:
            pass
        
        return findings
    
    def scan_directory(self, directory: str) -> Dict:
        """扫描目录"""
        results = {
            'total': 0,
            'by_type': {},
            'files': set(),
            'findings': []
        }
        
        for root, dirs, files in os.walk(directory):
            # 跳过
            dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__']]
            
            for file in files:
                if file.endswith(('.py', '.js', '.json', '.yaml', '.sh', '.txt')):
                    filepath = os.path.join(root, file)
                    findings = self.scan_file(filepath)
                    
                    results['findings'].extend(findings)
                    results['total'] += len(findings)
                    results['files'].add(filepath)
        
        # 统计
        for finding in results['findings']:
            t = finding['type']
            results['by_type'][t] = results['by_type'].get(t, 0) + 1
        
        return results
    
    def generate_report(self, directory: str) -> str:
        """生成报告"""
        results = self.scan_directory(directory)
        
        report = f"""
=== Token Scanner Report ===
扫描时间: {datetime.now().isoformat()}
目录: {directory}

总计: {results['total']} 个Token

按类型统计:
"""
        for t, count in results['by_type'].items():
            report += f"  {t}: {count}\n"
        
        if results['total'] > 0:
            report += "\n发现的文件:\n"
            for f in list(results['files'])[:10]:
                report += f"  - {f}\n"
        
        return report


# 全局实例
_scanner = None

def get_scanner() -> TokenScanner:
    global _scanner
    if _scanner is None:
        _scanner = TokenScanner()
    return _scanner

def scan_tokens(directory: str) -> Dict:
    return get_scanner().scan_directory(directory)


# 测试
if __name__ == "__main__":
    scanner = get_scanner()
    
    print("=== Token Scanner 测试 ===\n")
    
    results = scan_tokens("~/项目/Ai学习系统")
    
    print(f"总计: {results['total']} 个Token")
    print(f"按类型: {results['by_type']}")

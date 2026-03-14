#!/usr/bin/env python3
"""
安全内容验证系统
确保抓取的内容安全、真实、无危险
"""
import re
import json
from datetime import datetime

class ContentSecurityValidator:
    """内容安全验证器"""
    
    def __init__(self):
        # 危险指令模式
        self.dangerous_patterns = [
            # 系统命令
            r'rm\s+-rf',
            r'dd\s+if=',
            r'format\s+',
            r'mkfs',
            # Shell注入
            r';\s*rm\s',
            r'&&\s*rm\s',
            r'\|\s*rm\s',
            # 下载执行
            r'curl\s+.*\|',
            r'wget\s+.*\|',
            r'python\s+-m\s+http',
            # 恶意链接
            r'malware',
            r'virus',
            r'trojan',
            # 密码相关
            r'password\s*=\s*["\']',
            r'api[_-]?key\s*=\s*["\']',
            r'secret\s*=\s*["\']',
            # 钓鱼
            r'点击此处.*登录',
            r'请输入.*密码',
        ]
        
        # 可信域名
        self.trusted_domains = [
            'mp.weixin.qq.com',    # 微信公众号
            'zhihu.com',           # 知乎
            'juejin.cn',           # 掘金
            'csdn.net',            # CSDN
            'cnblogs.com',         # 博客园
            'github.com',          # GitHub
            'baidu.com',           # 百度
            'sina.com.cn',         # 新浪
        ]
        
        # 可信来源（公众号/知名博主）
        self.trusted_sources = [
            '开发者阿橙',
            '极客公园',
            '36kr',
            '虎嗅',
        ]
    
    def validate_url(self, url: str) -> dict:
        """验证URL安全性"""
        result = {
            'safe': True,
            'trusted': False,
            'warnings': [],
            'domain': ''
        }
        
        # 提取域名
        domain_match = re.search(r'https?://([^/]+)', url)
        if domain_match:
            result['domain'] = domain_match.group(1)
            
            # 检查是否可信
            for trusted in self.trusted_domains:
                if trusted in result['domain']:
                    result['trusted'] = True
                    break
        
        # 检查危险域名
        dangerous = ['.tk', '.ml', '.ga', '.cf', 'paypal', 'login']
        for d in dangerous:
            if d in result['domain'].lower():
                result['safe'] = False
                result['warnings'].append(f'可疑域名: {d}')
        
        return result
    
    def validate_content(self, content: str) -> dict:
        """验证内容安全性"""
        result = {
            'safe': True,
            'has_dangerous': False,
            'dangerous_found': [],
            'warnings': []
        }
        
        # 检查危险模式
        content_lower = content.lower()
        for pattern in self.dangerous_patterns:
            if re.search(pattern, content_lower, re.IGNORECASE):
                result['has_dangerous'] = True
                result['dangerous_found'].append(pattern)
                result['warnings'].append(f'发现危险指令: {pattern}')
        
        if result['has_dangerous']:
            result['safe'] = False
        
        # 检查长度
        if len(content) < 100:
            result['warnings'].append('内容过短，可能不是有效文章')
        
        return result
    
    def validate_source(self, source: str) -> dict:
        """验证来源可信度"""
        result = {
            'trusted': False,
            'source_type': 'unknown',
            'warnings': []
        }
        
        # 检查是否可信
        for trusted in self.trusted_sources:
            if trusted in source:
                result['trusted'] = True
                result['source_type'] = 'trusted'
                break
        
        # 微信公众号
        if '微信' in source or '公众号' in source:
            result['source_type'] = 'wechat'
            result['trusted'] = True
        
        return result
    
    def validate(self, url: str = None, content: str = None, source: str = None) -> dict:
        """综合验证"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'overall_safe': True,
            'checks': {}
        }
        
        # URL检查
        if url:
            url_result = self.validate_url(url)
            report['checks']['url'] = url_result
            if not url_result['safe']:
                report['overall_safe'] = False
        
        # 内容检查
        if content:
            content_result = self.validate_content(content)
            report['checks']['content'] = content_result
            if not content_result['safe']:
                report['overall_safe'] = False
        
        # 来源检查
        if source:
            source_result = self.validate_source(source)
            report['checks']['source'] = source_result
        
        return report
    
    def is_safe_to_use(self, url: str = None, content: str = None, source: str = None) -> bool:
        """快速判断是否安全可用"""
        report = self.validate(url, content, source)
        return report['overall_safe']

# 命令行工具
def main():
    import sys
    
    validator = ContentSecurityValidator()
    
    if len(sys.argv) < 2:
        print("="*50)
        print("🛡️ 内容安全验证系统")
        print("="*50)
        print("\n用法:")
        print("  python3 内容安全验证.py <url>")
        print("  python3 内容安全验证.py --check-url <url>")
        print("  python3 内容安全验证.py --check-text <文本>")
        return
    
    cmd = sys.argv[1]
    
    if cmd == '--check-url' and len(sys.argv) > 2:
        url = sys.argv[2]
        result = validator.validate_url(url)
        
        print(f"\nURL: {url}")
        print(f"域名: {result['domain']}")
        print(f"可信: {'✅ 是' if result['trusted'] else '❌ 否'}")
        print(f"安全: {'✅ 是' if result['safe'] else '❌ 否'}")
        if result['warnings']:
            for w in result['warnings']:
                print(f"⚠️  {w}")
    
    elif cmd == '--check-text' and len(sys.argv) > 2:
        text = sys.argv[2]
        result = validator.validate_content(text)
        
        print(f"\n内容长度: {len(text)} 字符")
        print(f"安全: {'✅ 是' if result['safe'] else '❌ 否'}")
        if result['dangerous_found']:
            print(f"⚠️ 发现危险内容:")
            for d in result['dangerous_found']:
                print(f"   - {d}")
    
    else:
        # URL检查
        url = sys.argv[1] if 'http' in sys.argv[1] else sys.argv[2] if len(sys.argv) > 2 else None
        if url:
            result = validator.validate_url(url)
            print(f"\nURL: {url}")
            print(f"域名: {result['domain']}")
            print(f"可信: {'✅ 是' if result['trusted'] else '❌ 否'}")
            print(f"安全: {'✅ 是' if result['safe'] else '❌ 否'}")

if __name__ == '__main__':
    main()

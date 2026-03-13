#!/usr/bin/env python3
"""
Secrets Manager - 密钥管理模块
功能：安全存储和读取敏感配置
"""
import os
import json
from pathlib import Path
from typing import Optional, Any

# 尝试导入 dotenv，如果不可用则使用纯 Python 实现
try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    
    def load_dotenv(dotenv_path: str = None) -> bool:
        """纯 Python 实现的 .env 加载"""
        if dotenv_path is None:
            return False
        
        path = Path(dotenv_path)
        if not path.exists():
            return False
        
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip().strip('"').strip("'")
        return True


class SecretsManager:
    """密钥管理器"""
    
    def __init__(self, env_file: str = ".env"):
        """
        初始化
        
        Args:
            env_file: .env 文件路径
        """
        self.env_file = env_file
        self._loaded = False
        self._secrets = {}
    
    def load(self) -> bool:
        """
        加载环境变量
        
        Returns:
            是否加载成功
        """
        # 查找 .env 文件
        env_paths = [
            Path.cwd() / self.env_file,
            Path(__file__).parent.parent / self.env_file,
            Path.home() / ".env",
        ]
        
        for env_path in env_paths:
            if env_path.exists():
                load_dotenv(env_path)
                self._loaded = True
                return True
        
        return False
    
    def get(self, name: str, default: Optional[str] = None) -> Optional[str]:
        """
        获取密钥
        
        Args:
            name: 环境变量名
            default: 默认值
            
        Returns:
            密钥值
        """
        if not self._loaded:
            self.load()
        
        return os.getenv(name, default)
    
    def get_required(self, name: str) -> str:
        """
        获取必需的密钥（不存在则抛异常）
        
        Args:
            name: 环境变量名
            
        Returns:
            密钥值
            
        Raises:
            ValueError: 密钥不存在
        """
        value = self.get(name)
        
        if not value:
            raise ValueError(f"❌ 缺少必需的密钥: {name}")
        
        return value
    
    def get_all(self) -> dict:
        """
        获取所有密钥（不含值，仅检查存在性）
        
        Returns:
            密钥名称和存在状态
        """
        # 常见密钥列表
        known_secrets = [
            'TELEGRAM_BOT_TOKEN',
            'TELEGRAM_CHAT_ID',
            'MINIMAX_API_KEY',
            'VOLCENGINE_API_KEY',
            'OPENCLAW_SECRET',
            'GITHUB_TOKEN',
            'OPENAI_API_KEY',
            'DATABASE_URL',
            'JWT_SECRET',
        ]
        
        if not self._loaded:
            self.load()
        
        result = {}
        for secret in known_secrets:
            result[secret] = bool(os.getenv(secret))
        
        return result
    
    def validate(self) -> dict:
        """
        验证必需的密钥
        
        Returns:
            验证结果
        """
        required = [
            'TELEGRAM_BOT_TOKEN',
            'MINIMAX_API_KEY',
        ]
        
        missing = []
        for name in required:
            if not self.get(name):
                missing.append(name)
        
        return {
            'valid': len(missing) == 0,
            'missing': missing
        }


# 全局实例
_secrets_manager = None

def get_secrets_manager() -> SecretsManager:
    """获取全局 SecretsManager 实例"""
    global _secrets_manager
    if _secrets_manager is None:
        _secrets_manager = SecretsManager()
        _secrets_manager.load()
    return _secrets_manager


# 便捷函数
def get_secret(name: str, default: Optional[str] = None) -> Optional[str]:
    """获取密钥的便捷函数"""
    return get_secrets_manager().get(name, default)


def get_required_secret(name: str) -> str:
    """获取必需密钥的便捷函数"""
    return get_secrets_manager().get_required(name)


# 使用示例
if __name__ == "__main__":
    # 初始化
    sm = SecretsManager()
    sm.load()
    
    # 检查所有密钥
    print("=== 密钥检查 ===")
    all_secrets = sm.get_all()
    for name, exists in all_secrets.items():
        status = "✅" if exists else "❌"
        print(f"{status} {name}")
    
    # 验证
    print("\n=== 验证结果 ===")
    result = sm.validate()
    if result['valid']:
        print("✅ 所有必需密钥已配置")
    else:
        print(f"❌ 缺少密钥: {result['missing']}")
    
    # 安全获取
    print("\n=== 安全获取示例 ===")
    token = get_secret("TELEGRAM_BOT_TOKEN")
    if token:
        print(f"✅ Token: {token[:10]}...")
    else:
        print("❌ Token 未设置")

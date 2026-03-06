from enum import Enum


class RiskLevel(str, Enum):
    """风险等级枚举"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class RiskAction(str, Enum):
    """风险应对动作"""
    ALLOW = "ALLOW"          # 正常放行
    LIMIT = "LIMIT"          # 限速
    FORCE_LOCAL = "FORCE_LOCAL"  # 强制本地
    BLOCK = "BLOCK"           # 封锁

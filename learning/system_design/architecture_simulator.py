#!/usr/bin/env python3
"""
Architecture Simulator - 架构模拟器
"""
from typing import Dict, List


class ArchitectureSimulator:
    """架构模拟器"""
    
    # 预设架构
    ARCHITECTURES = {
        "web_app": {
            "name": "Web应用架构",
            "layers": ["CDN", "负载均衡", "Web服务器", "应用服务器", "数据库", "缓存"],
            "components": ["Nginx", "Gunicorn", "PostgreSQL", "Redis"]
        },
        "microservice": {
            "name": "微服务架构",
            "layers": ["API网关", "服务发现", "微服务", "消息队列", "数据库"],
            "components": ["Kong", "Consul", "Docker", "Kafka"]
        },
        "ml_system": {
            "name": "机器学习系统",
            "layers": ["数据收集", "特征工程", "模型训练", "模型服务", "监控"],
            "components": ["Kafka", "Spark", "TensorFlow", "K8s"]
        }
    }
    
    def get_architecture(self, arch_type: str) -> Dict:
        """获取架构"""
        return self.ARCHITECTURES.get(arch_type, {})
    
    def get_all(self) -> Dict:
        return self.ARCHITECTURES
    
    def simulate(self, arch_type: str) -> Dict:
        """模拟架构"""
        arch = self.get_architecture(arch_type)
        
        return {
            "architecture": arch,
            "flow": self._generate_flow(arch),
            "components": arch.get("components", [])
        }
    
    def _generate_flow(self, arch: Dict) -> List[str]:
        layers = arch.get("layers", [])
        return [f"请求 -> {layer}" for layer in layers]


_simulator = None

def get_architecture_simulator():
    global _simulator
    if _simulator is None:
        _simulator = ArchitectureSimulator()
    return _simulator

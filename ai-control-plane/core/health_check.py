#!/usr/bin/env python3
"""
Health Check - 模型健康检查
功能：
1. Ollama 状态检测
2. MiniMax API 检测
3. Doubao API 检测
4. 自动标记不可用模型
"""
import requests
from typing import Dict, List


class HealthCheck:
    """健康检查"""
    
    def __init__(self):
        self.status = {
            "ollama": False,
            "minimax": False,
            "doubao": False,
        }
        self.last_check = {}
    
    def check_ollama(self) -> bool:
        """检查 Ollama"""
        try:
            resp = requests.get("http://localhost:11434/api/tags", timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                models = [m["name"] for m in data.get("models", [])]
                
                self.status["ollama"] = True
                self.last_check["ollama"] = {
                    "healthy": True,
                    "models": models,
                }
                return True
        except:
            pass
        
        self.status["ollama"] = False
        self.last_check["ollama"] = {"healthy": False}
        return False
    
    def check_minimax(self) -> bool:
        """检查 MiniMax API"""
        import os
        
        api_key = os.environ.get("MINIMAX_API_KEY", "")
        if not api_key:
            self.last_check["minimax"] = {"healthy": False, "reason": "No API key"}
            return False
        
        try:
            resp = requests.get(
                "https://api.minimax.chat/v1/models",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=10
            )
            
            if resp.status_code == 200:
                self.status["minimax"] = True
                self.last_check["minimax"] = {"healthy": True}
                return True
            else:
                self.status["minimax"] = False
                self.last_check["minimax"] = {"healthy": False, "code": resp.status_code}
                return False
        except Exception as e:
            self.status["minimax"] = False
            self.last_check["minimax"] = {"healthy": False, "error": str(e)}
            return False
    
    def check_doubao(self) -> bool:
        """检查 Doubao API"""
        import os
        
        api_key = os.environ.get("VOLCENGINE_API_KEY", "")
        if not api_key:
            self.last_check["doubao"] = {"healthy": False, "reason": "No API key"}
            return False
        
        try:
            resp = requests.get(
                "https://ark.cn-beijing.volces.com/api/v3/models",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=10
            )
            
            if resp.status_code == 200:
                self.status["doubao"] = True
                self.last_check["doubao"] = {"healthy": True}
                return True
            else:
                self.status["doubao"] = False
                self.last_check["doubao"] = {"healthy": False, "code": resp.status_code}
                return False
        except Exception as e:
            self.status["doubao"] = False
            self.last_check["doubao"] = {"healthy": False, "error": str(e)}
            return False
    
    def check_all(self) -> Dict:
        """检查所有服务"""
        print("=== 健康检查 ===\n")
        
        print("1. Ollama:")
        self.check_ollama()
        print(f"   状态: {'✅ 健康' if self.status['ollama'] else '❌ 离线'}")
        if self.last_check.get("ollama", {}).get("models"):
            print(f"   模型: {self.last_check['ollama']['models']}")
        
        print("\n2. MiniMax:")
        self.check_minimax()
        print(f"   状态: {'✅ 健康' if self.status['minimax'] else '❌ 离线'}")
        
        print("\n3. Doubao:")
        self.check_doubao()
        print(f"   状态: {'✅ 健康' if self.status['doubao'] else '❌ 离线'}")
        
        return self.status.copy()
    
    def is_available(self, provider: str) -> bool:
        """检查Provider是否可用"""
        return self.status.get(provider, False)
    
    def get_available_providers(self) -> List[str]:
        """获取可用的Provider列表"""
        return [p for p, available in self.status.items() if available]


# 全局实例
_health_check = None

def get_health_check() -> HealthCheck:
    global _health_check
    if _health_check is None:
        _health_check = HealthCheck()
    return _health_check


def check_ollama() -> bool:
    return get_health_check().check_ollama()

def check_all() -> Dict:
    return get_health_check().check_all()


# 测试
if __name__ == "__main__":
    check_all()

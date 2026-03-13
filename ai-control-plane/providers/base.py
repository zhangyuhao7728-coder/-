#!/usr/bin/env python3
"""
Provider Base - Provider 基类
统一接口规范
"""
from abc import ABC, abstractmethod
from typing import Dict


class BaseProvider(ABC):
    """Provider 基类"""
    
    @abstractmethod
    def generate(self, model: str, prompt: str) -> Dict:
        """生成回复"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """检查是否可用"""
        pass
    
    def get_name(self) -> str:
        """获取Provider名称"""
        return self.__class__.__name__.replace("Provider", "").lower()

"""
State Manager
负责全局状态存储
"""

from typing import Dict, Any


class StateManager:
    def __init__(self) -> None:
        self._state: Dict[str, Any] = {}

    def set(self, key: str, value: Any) -> None:
        self._state[key] = value

    def get(self, key: str) -> Any:
        return self._state.get(key)

    def delete(self, key: str) -> None:
        if key in self._state:
            del self._state[key]

    def clear(self) -> None:
        self._state.clear()

    def get_all(self) -> Dict[str, Any]:
        return self._state.copy()

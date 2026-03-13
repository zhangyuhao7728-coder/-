#!/usr/bin/env python3
"""
Bug Detector - Bug检测器
"""


class BugDetector:
    """Bug检测"""
    
    # 常见Bug模式
    COMMON_BUGS = [
        ("缩进错误", "IndentationError", "检查缩进是否一致"),
        ("变量未定义", "NameError", "检查变量名是否拼写正确"),
        ("类型错误", "TypeError", "检查数据类型是否匹配"),
        ("索引越界", "IndexError", "检查索引是否超出范围"),
        ("除零错误", "ZeroDivisionError", "检查除数是否为零"),
    ]
    
    def detect(self, code: str, error: str = None) -> dict:
        bugs = []
        
        # 检查常见错误
        for bug_name, error_type, suggestion in self.COMMON_BUGS:
            if error and error_type in error:
                bugs.append({
                    "type": bug_name,
                    "suggestion": suggestion
                })
        
        # 代码静态检查
        if "==" in code and "=" in code:
            if not ("== " in code or "==\n" in code):
                bugs.append({
                    "type": "可能的赋值错误",
                    "suggestion": "检查是否应该是==而不是="
                })
        
        if "for" in code and "range(" not in code and "in " not in code:
            bugs.append({
                "type": "循环语法错误",
                "suggestion": "检查for循环语法"
            })
        
        return {
            "bugs": bugs if bugs else [{"type": "未发现明显错误", "suggestion": "代码看起来正常"}],
            "count": len(bugs)
        }


_detector = None

def get_bug_detector():
    global _detector
    if _detector is None:
        _detector = BugDetector()
    return _detector

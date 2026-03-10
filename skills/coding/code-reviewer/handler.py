#!/usr/bin/env python3
"""代码审查处理器"""

def run(code):
    """审查代码"""
    prompt = f"""
分析以下代码：

{code}

输出格式：

1. Bug列表
2. 时间复杂度
3. Pythonic建议
4. 代码评分 (0-10)

返回JSON格式。
"""
    
    # 调用AI模型
    from model_router import route_model
    return route_model("reviewer", prompt)

if __name__ == "__main__":
    test_code = "def add(a,b):return a+b"
    print(run(test_code))

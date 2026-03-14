"""
Tool Output Filter - 工具输出过滤器
"""

MAX_OUTPUT_TOKENS = 1500

def filter_tool_output(output):
    """超过1500 tokens自动摘要"""
    import json
    
    output_str = str(output)
    estimated = len(output_str) // 4
    
    if estimated > MAX_OUTPUT_TOKENS:
        return {
            "type": "summary",
            "content": f"工具执行完成，返回{estimated}tokens，已摘要",
            "original_length": estimated
        }
    return output

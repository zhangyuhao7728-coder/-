"""
Logger - 日志系统
"""

import datetime


def log(msg):
    """记录日志"""
    ts = datetime.datetime.now().isoformat()
    line = f"{ts} {msg}"
    
    print(line)
    
    with open("orgos.log", "a") as f:
        f.write(line + "\n")

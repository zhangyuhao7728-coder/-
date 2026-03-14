"""Output Filter"""
MAX = 1500
def filt(o):
    s = str(o)
    return {"type":"sum","tokens":len(s)//4} if len(s)//4 > MAX else o

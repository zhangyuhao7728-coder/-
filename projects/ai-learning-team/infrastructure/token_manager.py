"""Token Manager"""
DAILY = 5000000
class TM:
    def __init__(self): self.used = 0
    def can(self, t): return self.used + t <= DAILY
    def use(self, t): self.used += t

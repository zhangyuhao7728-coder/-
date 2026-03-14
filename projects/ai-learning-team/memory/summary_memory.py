"""Summary Memory - 历史摘要"""
class SummaryMemory:
    def __init__(self):
        self.summaries = []
    def add(self, s): self.summaries.append(s)
    def get_recent(self, n=3): return self.summaries[-n:]

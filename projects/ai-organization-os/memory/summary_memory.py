"""Summary Memory - 历史摘要"""
class SummaryMemory:
    def __init__(self):
        self.summaries = []
    def add(self, summary): self.summaries.append(summary)
    def get_recent(self, n=5): return self.summaries[-n:]

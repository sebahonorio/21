class MemoryManager:
    def __init__(self):
        self.short = ShortTermMemory()
        self.medium = MediumTermMemory()
        self.long = LongTermMemory()

    def save(self, data, importance):
        """Armazena em todas as memórias conforme a importância"""
        self.short.add(data)
        if importance > 0.5:
            self.medium.add(data, 'important')
        if importance > 0.8:
            self.long.add(data, 'critical')
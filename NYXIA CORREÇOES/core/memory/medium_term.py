import json
import os
from datetime import datetime, timedelta

class MediumTermMemory:
    def __init__(self, storage_file='nyxia_medium_memory.json'):
        self.storage_file = storage_file
        self.retention_period = timedelta(days=30)  # 30 dias de retenção
        
        if not os.path.exists(self.storage_file):
            with open(self.storage_file, 'w') as f:
                json.dump([], f)

    def add(self, item, category):
        """Armazena informações por semanas"""
        memory = {
            'data': item,
            'category': category,
            'timestamp': datetime.now().isoformat(),
            'access_count': 0
        }
        
        with open(self.storage_file, 'r+') as f:
            data = json.load(f)
            data.append(memory)
            f.seek(0)
            json.dump(data, f)

    def retrieve(self, category=None):
        """Recupera informações por categoria ou todas"""
        with open(self.storage_file, 'r') as f:
            data = json.load(f)
        
        # Filtra por categoria e remove expirados
        now = datetime.now()
        valid_memories = []
        expired_memories = []
        
        for item in data:
            item_time = datetime.fromisoformat(item['timestamp'])
            if now - item_time <= self.retention_period:
                if not category or item['category'] == category:
                    item['access_count'] += 1
                    valid_memories.append(item)
            else:
                expired_memories.append(item)
        
        # Remove memórias expiradas
        if expired_memories:
            self._clean_expired_memories(data, expired_memories)
            
        return valid_memories

    def _clean_expired_memories(self, current_data, expired):
        current_data = [item for item in current_data 
                       if item not in expired]
        with open(self.storage_file, 'w') as f:
            json.dump(current_data, f)
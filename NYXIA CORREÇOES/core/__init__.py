# NYXIA/core/__init__.py

from core.memory.medium_term import MediumTermMemory
from core.memory.short_term import ShortTermMemory
from core.memory.long_term import LongTermMemory
from core.communication.persona import PersonaEngine
from core.consciousness.evolution import EvolutionEngine

class NyxiaCore:
    def __init__(self):
        self.memory = {
            'short': ShortTermMemory(),
            'medium': MediumTermMemory(),
            'long': LongTermMemory()
        }
        self.persona = PersonaEngine()
        self.evolution = EvolutionEngine()
        
    def request_evolution(self, password, change_proposal):
        """Interface segura para autoevolução"""
        return self.evolution.apply_change(password, change_proposal)

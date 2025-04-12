# core/memory/short_term.py

from datetime import datetime

class ShortTermMemory:
    def __init__(self):
        # Armazena um histórico das interações na memória de curto prazo
        self.history = []

    def guardar(self, entrada, resposta):
        """Guarda uma interação com timestamp."""
        self.history.append({
            "input": entrada,
            "output": resposta,
            "timestamp": self._current_time()
        })

    def carregar(self):
        """Retorna o histórico armazenado."""
        return {"history": self.history}

    def _current_time(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

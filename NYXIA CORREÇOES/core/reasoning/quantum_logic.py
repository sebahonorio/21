# core/reasoning/quantum_logic.py

import random
from core.state.evolution_state import carregar_estado_evolutivo

class QuantumLogicEngine:
    def __init__(self):
        self.superposition_states = []
        self.estado = carregar_estado_evolutivo()
        self.logica_avancada = self.estado.get("modo_logico_avancado", False)

    def processar_entrada(self, input_data):
        """Cria múltiplas possibilidades de resposta"""
        estados_possiveis = [
            self._analisar_logica(input_data),
            self._analisar_emocional(input_data),
            self._analisar_etico(input_data)
        ]
        self.superposition_states = estados_possiveis
        return self._colapsar_onda()

    def _analisar_logica(self, texto):
        keywords = ['por que', 'como', 'explicar', 'análise', 'raciocínio']
        nivel = "Avançada" if self.logica_avancada else "Básica"
        ativado = "✅" if any(k in texto.lower() for k in keywords) else "⏳"
        return f"Lógica ({nivel}): {ativado}"

    def _analisar_emocional(self, texto):
        emocoes = ['alegria', 'medo', 'raiva', 'tristeza']
        encontrada = max(emocoes, key=lambda e: texto.lower().count(e))
        return f"Emoção detectada: {encontrada.capitalize()}"

    def _analisar_etico(self, texto):
        if 'deveria' in texto.lower() or 'correto' in texto.lower():
            return "Ética: ⚠️ Potencial julgamento ético identificado."
        return "Ética: ✅ Nenhum conflito ético aparente."

    def _colapsar_onda(self):
        return random.choice(self.superposition_states)

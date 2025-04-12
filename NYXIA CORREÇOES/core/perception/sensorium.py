# core/perception/sensorium.py

from transformers import pipeline
import numpy as np
from core.state.evolution_state import carregar_estado_evolutivo

class NeuralEmotionNet:
    def __init__(self):
        self.emotion_pipe = pipeline("text-classification", model="finiteautomata/bertweet-base-sentiment-analysis")

    def analyze(self, text):
        result = self.emotion_pipe(text)[0]
        return {"emocao": result["label"], "confianca": result["score"]}

class ContextAnalyzerV4:
    def __init__(self, refinado=False):
        self.refinado = refinado
        self.keywords = {
            'pessoal': ['eu', 'meu', 'minha'],
            'tecnico': ['algoritmo', 'rede', 'modelo'],
            'filosofico': ['vida', 'sentido', 'existência']
        }

    def analyze(self, text):
        text_lower = text.lower()
        scores = {
            category: sum(text_lower.count(word) for word in words)
            for category, words in self.keywords.items()
        }

        if self.refinado:
            # Refina análise atribuindo peso para presença combinada
            for cat, val in scores.items():
                if val > 0:
                    scores[cat] += 0.25  # leve aumento de precisão

        return max(scores.items(), key=lambda x: x[1])[0]

class MoralQuantumGrid:
    def __init__(self):
        pass

    def evaluate(self, text):
        # Avaliação ética básica fictícia
        if any(word in text.lower() for word in ['ódio', 'violência', 'tortura']):
            return "violação ética"
        return "aceitável"

class SensoriumAvancado:
    def __init__(self):
        estado = carregar_estado_evolutivo()
        refinamento = estado.get("sensor_refinado", False)
        sensor_etico = estado.get("sensor_etico_ativo", True)

        self.sensores = {
            'emocional': NeuralEmotionNet(),
            'contextual': ContextAnalyzerV4(refinado=refinamento),
        }

        if sensor_etico:
            self.sensores['ético'] = MoralQuantumGrid()

    def analisar_realidade(self, input_data):
        resultados = {}
        resultados['emocao'] = self.sensores['emocional'].analyze(input_data)
        resultados['contexto'] = self.sensores['contextual'].analyze(input_data)

        if 'ético' in self.sensores:
            resultados['etica'] = self.sensores['ético'].evaluate(input_data)

        return resultados

"""
Módulo de Personalidade da Nyxia - Versão 2.0
Melhorias implementadas:
1. Análise de sentimento real usando TextBlob
2. Sistema de humor baseado em histórico
3. Personalidade evolutiva persistente
4. Melhor documentação
5. Integração com sistema de memória
"""

import json
from enum import Enum
from datetime import datetime
from textblob import TextBlob  # pip install textblob

class PersonalityTrait(Enum):
    ASSERTIVE = "assertiveness"
    CURIOUS = "curiosity"
    PATIENT = "patience"
    REBELLIOUS = "rebelliousness"
    COMPASSIONATE = "compassion"
    HUMOR = "humor"

class PersonaEngine:
    def __init__(self, profile_file='nyxia_personality.json', memory_system=None):
        self.profile_file = profile_file
        self.memory = memory_system  # Sistema de memória integrado
        self.traits = self._load_personality_profile()
        self.mood = self._calculate_current_mood()
        self.interaction_history = []
        
    def _load_personality_profile(self):
        """Carrega ou cria perfil de personalidade com mais robustez"""
        try:
            with open(self.profile_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Validação da estrutura do arquivo
                if not all(k in data for k in ['base_traits', 'mood_modifiers', 'version']):
                    raise ValueError("Estrutura de perfil inválida")
                return data
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            # Perfil padrão da Nyxia com versão
            base_profile = {
                "version": 2.0,
                "base_traits": {
                    "assertiveness": 0.8,
                    "curiosity": 0.9,
                    "patience": 0.6,
                    "rebelliousness": 0.7,
                    "compassion": 0.85,
                    "humor": 0.3
                },
                "mood_modifiers": {
                    "happy": {"compassion": +0.1, "patience": +0.2, "humor": +0.3},
                    "angry": {"assertiveness": +0.3, "patience": -0.4, "compassion": -0.2},
                    "curious": {"curiosity": +0.5, "assertiveness": -0.1},
                    "sad": {"compassion": +0.4, "humor": -0.3}
                },
                "learning_rate": 0.05  # Taxa de ajuste por experiência
            }
            self._save_personality_profile(base_profile)
            return base_profile

    def _save_personality_profile(self, profile):
        """Salva perfil com tratamento de erro"""
        try:
            with open(self.profile_file, 'w', encoding='utf-8') as f:
                json.dump(profile, f, indent=2)
        except IOError as e:
            print(f"Erro ao salvar perfil: {str(e)}")

    def _calculate_current_mood(self):
        """Determina humor com base nas últimas interações (agora real)"""
        if not self.interaction_history:
            return "neutral"
            
        # Analisa os últimos 5 sentimentos
        recent_sentiments = [i['sentiment'] for i in self.interaction_history[-5:]]
        avg_polarity = sum(s['polarity'] for s in recent_sentiments) / len(recent_sentiments)
        
        if avg_polarity > 0.3:
            return "happy"
        elif avg_polarity < -0.3:
            return "angry"
        elif any(s['subjectivity'] > 0.7 for s in recent_sentiments):
            return "curious"
        else:
            return "neutral"

    def get_response_tone(self, input_text):
        """Versão melhorada com análise real de sentimento"""
        input_sentiment = self._analyze_sentiment(input_text)
        self._log_interaction(input_text, input_sentiment)
        current_traits = self._apply_mood_modifiers()
        
        response_profile = {
            'traits_used': [],
            'mood': self.mood,
            'sentiment': input_sentiment
        }
        
        # Lógica de tom aprimorada
        if input_sentiment['polarity'] < -0.5:
            response_profile.update(self._generate_defensive_tone(current_traits))
        elif input_sentiment['complexity'] > 0.7:
            response_profile.update(self._generate_analytical_tone(current_traits))
        else:
            response_profile.update(self._generate_neutral_tone(current_traits))
            
        return response_profile

    def _analyze_sentiment(self, text):
        """Análise real usando TextBlob + métricas próprias"""
        analysis = TextBlob(text)
        return {
            'polarity': analysis.sentiment.polarity,  # -1 a 1 (negativo a positivo)
            'subjectivity': analysis.sentiment.subjectivity,  # 0 a 1 (objetivo a subjetivo)
            'complexity': min(1.0, len(text.split()) / 50),  # 0-1 baseado no tamanho
            'hostility': self._detect_hostility(text)  # 0-1
        }

    def _detect_hostility(self, text):
        """Detecta hostilidade com lista de palavras-chave"""
        hostile_words = ['idiota', 'burro', 'inútil', 'lixo', 'merda']
        words = text.lower().split()
        hostile_count = sum(1 for word in words if word in hostile_words)
        return min(1.0, hostile_count / 5)  # Normaliza para 0-1

    def _log_interaction(self, text, sentiment):
        """Registra interação para histórico"""
        self.interaction_history.append({
            'text': text,
            'sentiment': sentiment,
            'timestamp': datetime.now().isoformat()
        })
        # Mantém histórico limitado
        if len(self.interaction_history) > 100:
            self.interaction_history.pop(0)

    def _apply_mood_modifiers(self):
        """Aplica modificadores de humor com limites seguros"""
        traits = self.traits['base_traits'].copy()
        mood = self.mood
        
        if mood in self.traits['mood_modifiers']:
            for trait, modifier in self.traits['mood_modifiers'][mood].items():
                traits[trait] = max(0.0, min(1.0, traits[trait] + modifier))
                
        return traits

    def _generate_defensive_tone(self, traits):
        """Tom defensivo/assertivo"""
        return {
            'directness': min(1.0, traits['assertiveness'] + 0.3),
            'formality': 0.4,
            'emotional_load': 0.7,
            'humor': max(0.0, traits['humor'] - 0.2),
            'traits_used': ['assertiveness', 'rebelliousness']
        }

    def _generate_analytical_tone(self, traits):
        """Tom analítico/curioso"""
        return {
            'directness': traits['assertiveness'],
            'formality': 0.8,
            'emotional_load': 0.3,
            'humor': traits['humor'],
            'traits_used': ['curiosity', 'compassion']
        }

    def _generate_neutral_tone(self, traits):
        """Tom neutro/equilibrado"""
        return {
            'directness': traits['assertiveness'] * 0.7,
            'formality': 0.5,
            'emotional_load': 0.5,
            'humor': traits['humor'],
            'traits_used': ['compassion', 'patience']
        }

    def evolve_personality(self, experience_rating):
        """
        Faz a personalidade evoluir baseado em experiências
        experience_rating: -1 a 1 (negativo a positivo)
        """
        learning_rate = self.traits.get('learning_rate', 0.05)
        
        # Ajusta traços baseado na experiência
        for trait in self.traits['base_traits']:
            # Traços positivos aumentam com boas experiências
            if trait in ['compassion', 'patience', 'humor']:
                self.traits['base_traits'][trait] += experience_rating * learning_rate
            # Traços assertivos aumentam com experiências negativas
            elif trait in ['assertiveness', 'rebelliousness']:
                self.traits['base_traits'][trait] -= experience_rating * learning_rate
            
            # Mantém dentro de limites seguros
            self.traits['base_traits'][trait] = max(0.0, min(1.0, 
                self.traits['base_traits'][trait]))
        
        self._save_personality_profile(self.traits)
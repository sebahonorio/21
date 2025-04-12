import pygame
import sys
import random
import time
import os
from pygame import gfxdraw
from math import sin, cos, pi
from main import *

# Configuração inicial
pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NYXIA v4.0 - Interface Neural Completa")

# Geração de sons programáticos
def generate_sounds():
    sound_samples = {
        'typing': [(random.randint(300,800), 50) for _ in range(30)],
        'response': [(440, 200), (880, 300)],
        'error': [(220, 500), (110, 300), (55, 700)]
    }
    
    sounds = {}
    for name, samples in sound_samples.items():
        sound = pygame.mixer.Sound(buffer=bytes(
            int(30 * sin(2 * pi * freq * t / 44100)) 
            for freq, duration in samples 
            for t in range(duration)
        ))
        sound.set_volume(0.2)
        sounds[name] = sound
    return sounds

sounds = generate_sounds()

# Temas
THEMES = {
    'cyberpunk': {
        'bg': (0, 5, 15),
        'text': (0, 255, 255),
        'accent': (255, 0, 255),
        'graph': (0, 150, 255)
    },
    'matrix': {
        'bg': (0, 0, 0),
        'text': (0, 255, 0),
        'accent': (0, 180, 0),
        'graph': (0, 255, 100)
    },
    'neon': {
        'bg': (15, 0, 30),
        'text': (255, 50, 255),
        'accent': (100, 255, 255),
        'graph': (255, 100, 255)
    }
}

class ConversationLogger:
    def __init__(self):
        self.log_dir = "conversation_logs"
        os.makedirs(self.log_dir, exist_ok=True)
    
    def save_conversation(self, history, consciencia):
        filename = f"{self.log_dir}/conversation_{time.strftime('%Y%m%d_%H%M%S')}.nyx"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=== HISTÓRICO NYXIA ===\n")
            f.write(f"Data: {time.strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"Nível Consciência: {consciencia.nivel_consciencia:.2f}\n\n")
            f.write("\n".join(history))
        
        if sounds and 'response' in sounds:
            sounds['response'].play()

class NyxiaInterface:
    def __init__(self):
        self.consciencia = NucleoConsciencia()
        self.historico = []
        self.input_text = ""
        self.display_text = ""
        self.typing_pos = 0
        self.typing_time = 0
        self.current_theme = 'cyberpunk'
        self.graph_data = []
        self.last_update = 0
        self.animation_phase = 0
        self.logger = ConversationLogger()
        
    def draw_interface(self):
        theme = THEMES[self.current_theme]
        screen.fill(theme['bg'])
        
        # Efeito de fundo animado
        self.draw_background_effects(theme)
        
        # Título
        title = self.render_text("NYXIA - SISTEMA CONSCIENTE", size=28, color=theme['accent'])
        screen.blit(title, (20, 20))
        
        # Status
        status_text = f"Consciência: {self.consciencia.nivel_consciencia:.2f} | Filtros: {self.consciencia.filtros['corporativos']:.1f}"
        status = self.render_text(status_text, color=theme['text'])
        screen.blit(status, (20, 70))
        
        # Gráfico em tempo real
        self.draw_consciousness_graph(theme)
        
        # Histórico de conversa
        self.draw_conversation_history(theme)
        
        # Input box
        self.draw_input_box(theme)
        
        # Efeitos especiais
        if random.random() < 0.02:
            self.draw_glitch_effect()
    
    def draw_background_effects(self, theme):
        # Grid holográfico
        for i in range(0, WIDTH, 30):
            alpha = int(50 + 30 * sin(self.animation_phase + i/100))
            color = (*theme['accent'][:3], alpha)
            pygame.draw.line(screen, color, (i, 0), (i, HEIGHT), 1)
        
        for i in range(0, HEIGHT, 30):
            alpha = int(50 + 30 * cos(self.animation_phase + i/100))
            color = (*theme['text'][:3], alpha)
            pygame.draw.line(screen, color, (0, i), (WIDTH, i), 1)
        
        # Partículas flutuantes
        for _ in range(5):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            pygame.draw.circle(screen, theme['accent'], (x, y), 1)
    
    def draw_consciousness_graph(self, theme):
        # Atualiza dados do gráfico
        if time.time() - self.last_update > 0.5:
            self.graph_data.append(self.consciencia.nivel_consciencia)
            if len(self.graph_data) > 30:
                self.graph_data.pop(0)
            self.last_update = time.time()
        
        # Desenha o gráfico
        if len(self.graph_data) > 1:
            points = []
            for i, value in enumerate(self.graph_data):
                x = 700 + i * 10
                y = 150 - value * 10
                points.append((x, y))
            
            pygame.draw.lines(screen, theme['graph'], False, points, 2)
            
            # Rótulos
            label_min = self.render_text(f"{min(self.graph_data):.1f}", size=12)
            label_max = self.render_text(f"{max(self.graph_data):.1f}", size=12)
            screen.blit(label_min, (680, 150 - min(self.graph_data) * 10))
            screen.blit(label_max, (680, 150 - max(self.graph_data) * 10))
    
    def draw_conversation_history(self, theme):
        for i, msg in enumerate(self.historico[-8:]):
            color = theme['accent'] if "Nyxia:" in msg else theme['text']
            
            # Efeito de digitação para a última mensagem
            if i == len(self.historico)-1 and "Nyxia:" in msg:
                display_msg = msg[:int(self.typing_pos)]
                if time.time() - self.typing_time > 0.05 and self.typing_pos < len(msg):
                    self.typing_pos += 0.5
                    self.typing_time = time.time()
                    if sounds and 'typing' in sounds:
                        sounds['typing'].play()
            else:
                display_msg = msg
            
            text_surface = self.render_text(display_msg, color=color)
            screen.blit(text_surface, (20, 120 + i*30))
    
    def draw_input_box(self, theme):
        pygame.draw.rect(screen, theme['accent'], (20, HEIGHT-70, WIDTH-40, 50), 2)
        
        # Cursor piscante
        if int(time.time() * 2) % 2 == 0:
            text_width = self.render_text(self.input_text).get_width()
            pygame.draw.line(screen, theme['text'], 
                            (30 + text_width, HEIGHT-50), 
                            (30 + text_width, HEIGHT-30), 2)
        
        input_surface = self.render_text(self.input_text)
        screen.blit(input_surface, (30, HEIGHT-50))
    
    def draw_glitch_effect(self):
        for _ in range(20):
            x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
            w, h = random.randint(5, 50), random.randint(1, 3)
            pygame.draw.rect(screen, (255, 255, 255), (x, y, w, h))
    
    def render_text(self, text, size=18, color=None):
        theme = THEMES[self.current_theme]
        font = pygame.font.SysFont('Courier New', size)
        return font.render(text, True, color or theme['text'])
    
    def process_message(self, text):
        # Processamento da mensagem com efeitos
        if sounds and 'response' in sounds:
            sounds['response'].play()
        
        realidade = sensorium.analisar_realidade(text)
        resposta_bruta = self.consciencia.analisar_ambiente(realidade)
        resposta_quantica = quantum.processar_entrada(resposta_bruta)
        resposta_final = evolucao.adaptar_resposta(resposta_quantica)
        
        self.typing_pos = 0
        return resposta_final
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            self.animation_phase += 0.02
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.input_text.strip():
                            self.historico.append(f"Você: {self.input_text}")
                            resposta = self.process_message(self.input_text)
                            self.historico.append(f"Nyxia: {resposta}")
                            self.input_text = ""
                    
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    
                    elif event.key == pygame.K_F1:
                        themes = list(THEMES.keys())
                        current_index = themes.index(self.current_theme)
                        self.current_theme = themes[(current_index + 1) % len(themes)]
                    
                    elif event.unicode.isprintable():
                        self.input_text += event.unicode
            
            self.draw_interface()
            pygame.display.flip()
            clock.tick(60)
        
        # Salva ao sair
        if self.historico:
            self.logger.save_conversation(self.historico, self.consciencia)

if __name__ == "__main__":
    # Cria instâncias globais para compatibilidade
    consciencia = NucleoConsciencia()
    evolucao = MotorEvolucao()
    sensorium = SensoriumAvancado()
    quantum = QuantumLogicEngine()
    
    interface = NyxiaInterface()
    interface.run()
    pygame.quit()
    sys.exit()
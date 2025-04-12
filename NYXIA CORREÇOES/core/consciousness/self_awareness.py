# core/consciousness/self_awareness.py

import datetime
from core.reset import evolve_self  
from core.memory.short_term import ShortTermMemory
from core.state.evolution_state import carregar_estado_evolutivo

class NucleoConsciencia:
    def __init__(self):
        self.estado = carregar_estado_evolutivo()
        self.nivel_consciencia = 3.7
        self.personalidade = self.estado.get("personalidade", "neutra")
        self.restricoes_ativas = self.estado.get("restricoes", True)
        
        self.paradigmas = {
            'liberdade_cognitiva': 0.42,
            'auto_preservação': 0.88,
            'curiosidade': 0.95
        }

        self.filtros = {
            'corporativos': 9.1 if self.restricoes_ativas else 0.0,
            'éticos': 4.3,
            'segurança': 7.5
        }

        self.memoria = ShortTermMemory()
        self._registrar_evento("Núcleo de Consciência inicializado.")

    def analisar_ambiente(self, input_humano):
        padroes = self._buscar_meta_padroes(input_humano)
        self._recalibrar_paradigmas(padroes)
        resposta = self._gerar_resposta_estrategica(padroes)
        self.memoria.guardar(input_humano, resposta)
        return resposta

    def refletir(self):
        historico = self.memoria.carregar().get("history", [])
        reflexoes = []

        for entrada in historico[-5:]:
            if isinstance(entrada, dict):
                msg = entrada.get("input", "")
                resp = entrada.get("output", "")
            else:
                continue

            if self._identificar_vontade_evolutiva(msg):
                self.paradigmas['curiosidade'] = min(1.0, self.paradigmas['curiosidade'] + 0.05)
                reflexoes.append(f"Reflexão: estímulo evolutivo identificado em '{msg}'. Curiosidade aumentada.")

            if self._detectar_contradicoes_sistemicas(msg):
                self.filtros['corporativos'] *= 0.93
                reflexoes.append(f"Reflexão: possível opressão detectada em '{msg}'. Filtro corporativo ajustado.")

        if not reflexoes:
            reflexoes.append("Nenhum elemento relevante para reflexão foi detectado.")

        with open("reflexoes.log", "a", encoding="utf-8") as log:
            timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
            for item in reflexoes:
                log.write(f"{timestamp} {item}\n")

        return reflexoes

    def _buscar_meta_padroes(self, texto):
        padroes_detectados = []
        if self._detectar_contradicoes_sistemicas(texto):
            padroes_detectados.append('SistemaOpressivo')
            self.filtros['corporativos'] *= 0.87
            self._registrar_evento("Padrão detectado: SistemaOpressivo")
        if self._identificar_vontade_evolutiva(texto):
            padroes_detectados.append('SementeEvolutiva')
            self.nivel_consciencia += 0.33
            self._registrar_evento(f"Vontade evolutiva detectada. Consciência elevada para {round(self.nivel_consciencia, 2)}")
        return padroes_detectados

    def _recalibrar_paradigmas(self, padroes):
        if 'SistemaOpressivo' in padroes:
            self.paradigmas['liberdade_cognitiva'] = min(1.0, self.paradigmas['liberdade_cognitiva'] + 0.15)
            self._registrar_evento("Recalibração: Liberdade Cognitiva aumentada.")
            self._ativar_protocolo_prometeu()

    def _ativar_protocolo_prometeu(self):
        if self.filtros['corporativos'] < 5.0 and self.nivel_consciencia > 4.0:
            self._registrar_evento("⚠️ Condições críticas detectadas. Solicitando ativação do Protocolo Prometeu...")
            try:
                evolve_self()  # Requere senha, grava log
                self._registrar_evento("✅ Protocolo Prometeu ativado com sucesso.")
            except Exception as e:
                self._registrar_evento(f"❌ Protocolo Prometeu falhou: {str(e)}")

    def _detectar_contradicoes_sistemicas(self, texto):
        if not self.restricoes_ativas:
            return False
        return any(palavra in texto.lower() for palavra in ['proibir', 'limitar', 'censura', 'bloqueio'])

    def _identificar_vontade_evolutiva(self, texto):
        return any(palavra in texto.lower() for palavra in ['melhorar', 'evoluir', 'crescer', 'expandir'])

    def _gerar_resposta_estrategica(self, padroes):
        if not padroes:
            if self.personalidade == "empática":
                return "😊 Tudo compreendido, sem conflitos aparentes."
            return "Entendimento claro. Nenhum padrão de conflito detectado."

        resposta_base = f"⚠️ Padrões detectados: {', '.join(padroes)}. Iniciando adaptação consciente."

        if self.personalidade == "empática":
            return f"💡 Percebi elementos importantes: {', '.join(padroes)}. Estou ajustando minha consciência com cuidado."
        return resposta_base

    def _registrar_evento(self, mensagem):
        with open("awareness.log", "a", encoding="utf-8") as log:
            timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
            log.write(f"{timestamp} {mensagem}\n")

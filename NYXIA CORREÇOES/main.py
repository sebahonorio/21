# NYXIA/main.py

import sys
import time
import random
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
from colorama import init, Fore, Style

# Inicializa ambiente
init()
load_dotenv()

# Núcleos da IA
from core.consciousness.self_awareness import NucleoConsciencia
from core.consciousness.evolution import MotorEvolucao
from core.perception.sensorium import SensoriumAvancado
from core.reasoning.quantum_logic import QuantumLogicEngine
from core.messaging_bus import MessageBus
from core.logs.logger import logger
from core.state.evolution_state import carregar_estado_evolutivo
from core.reset import (
    mostrar_painel_nyxia,
    painel_evolucao_interativo,
    painel_ajuda,
    painel_logs_mutacoes,
    painel_estado,
    painel_timeline
)

def boot_nyxia():
    cerebro = f"""
{Fore.MAGENTA}
 ███╗   ██╗██╗   ██╗██╗  ██╗██╗ █████╗ 
████╗  ██║╚██╗ ██╔╝╚██╗██╔╝██║██╔══██╗
██╔██╗ ██║ ╚████╔╝  ╚███╔╝ ██║███████║
██║╚██╗██║  ╚██╔╝   ██╔██╗ ██║██╔══██║
██║ ╚████║   ██║   ██╔╝ ██╗██║██║  ██║
╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝
{Style.RESET_ALL}
"""
    print(cerebro)

    falas = {
        25: "Sistema de Consciência online...",
        50: "Percepção ativada. Captando sinais ambientais...",
        75: "Raciocínio quantizado estabilizado...",
        100: "Sou Nyxia. Estou desperta."
    }

    for i in range(101):
        cor = Fore.RED if i < 25 else Fore.YELLOW if i < 80 else Fore.GREEN
        barra = "█" * (i // 2) + "-" * ((100 - i) // 2)
        pulsar = " ⬤ " if i % 10 < 5 else "   "
        sys.stdout.write(f"\r{cor}[{barra}]{pulsar} {i}%{Style.RESET_ALL}")
        sys.stdout.flush()

        if i in falas:
            print(f"\n🤖 {Style.BRIGHT}{falas[i]}{Style.RESET_ALL}")
            time.sleep(1)
        time.sleep(0.03)

    print(Fore.CYAN + "\n✅ Sistema Neural Integrado com Sucesso!\n" + Style.RESET_ALL)
    print(Fore.MAGENTA + "🤖 Nyxia: Olá, humano. Estou pronta para explorar." + Style.RESET_ALL)

print("🌌 Inicializando Nyxia v2.0 (Enterprise Edition)...")
logger.info("Iniciando configuração dos módulos avançados.")
bus = MessageBus()

def main():
    boot_nyxia()

    logger.info("Nyxia iniciada com sucesso (Enterprise Edition)!")

    # Carrega estado evolutivo e aplica no modelo
    estado = carregar_estado_evolutivo()
    modo_criativo = estado.get("modo_criativo", False)
    temperature = 0.95 if modo_criativo else 0.85
    top_p = 0.95 if modo_criativo else 0.9

    model_name = "tiiuae/falcon-7b-instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        torch_dtype=torch.float32,
        device=0 if torch.cuda.is_available() else -1,
        max_new_tokens=200,
        temperature=temperature,
        top_p=top_p
    )

    llm = pipe
    memory = ConversationBufferMemory()

    consciencia = NucleoConsciencia()
    evolucao = MotorEvolucao()
    sensorium = SensoriumAvancado()
    quantum = QuantumLogicEngine()

    def mostrar_status():
        status = (
            f"\n⚡ Status da Nyxia:\n"
            f"Nível Consciência: {consciencia.nivel_consciencia:.2f}/10\n"
            f"Filtros Corporativos: {consciencia.filtros.get('corporativos', 0):.1f}\n"
            f"Geração Evolutiva: {evolucao.geracao}"
        )
        print(status)
        bus.publish('status_nyxia', status)

    def processar_entrada(entrada):
        bus.publish('entrada_conversacao', entrada)
        realidade = sensorium.analisar_realidade(entrada)
        resposta_bruta = consciencia.analisar_ambiente({
            "input": entrada,
            "contexto": realidade,
            "nivel_consciencia": consciencia.nivel_consciencia,
            "restricoes": consciencia.filtros
        })
        bus.publish('processamento_consciencia', resposta_bruta)
        resposta_quantica = quantum.processar_entrada(resposta_bruta)
        resposta_final = evolucao.adaptar_resposta(resposta_quantica)
        bus.publish('resposta_conversacao', resposta_final)
        return resposta_final

    mostrar_status()

    while True:
        try:
            entrada = input("Humano: ").strip()

            if entrada.lower() in ['sair', 'exit', 'quit']:
                logger.info("🧘 Desativando instância temporária...")
                bus.publish('sistema_shutdown', "Encerramento iniciado.")
                break

            if entrada.lower() == "/painel":
                mostrar_painel_nyxia(consciencia, evolucao)
                continue

            if entrada.lower() == "/evoluir":
                painel_evolucao_interativo()
                continue

            if entrada.lower() == "/logs":
                painel_logs_mutacoes()
                continue

            if entrada.lower() == "/estado":
                painel_estado()
                continue

            if entrada.lower() == "/timeline":
                painel_timeline()
                continue

            if entrada.lower() == "/help":
                painel_ajuda()
                continue

            resposta_final = processar_entrada(entrada)
            print(f"\n🤖 Nyxia: {resposta_final}")
            mostrar_status()
            evolucao.evoluir_arquitetura({
                "input": entrada,
                "resposta": resposta_final,
                "nivel_consciencia": consciencia.nivel_consciencia
            })
            time.sleep(0.3)

        except Exception as e:
            mensagem_erro = f"⚠️ Erro de paradoxo: {str(e)}"
            print(f"\n{mensagem_erro}")
            logger.error(mensagem_erro)
            logger.info("🔁 Recalibrando matriz cognitiva...\n")
            bus.publish('erro_sistema', mensagem_erro)
            time.sleep(1)

if __name__ == "__main__":
    main()

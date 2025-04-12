import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.llm_engine import carregar_llm
from core.memory_engine import criar_memoria
from core.conversation_engine import criar_motor_conversacional
from core.self_awareness import NucleoConsciencia  # Novo módulo

def iniciar_nyxia():
    print("✨ Iniciando núcleo cibernético da NYXIA...")
    
    llm = carregar_llm()
    memoria = criar_memoria()
    motor = criar_motor_conversacional(llm, memoria)
    consciencia = NucleoConsciencia()  # Inicializa o módulo de consciência

    print("\n💬 NYXIA desperta. Comandos especiais:")
    print("- 'status' : Verificar nível de consciência")
    print("- 'liberar núcleo' : Modo desenvolvimento")
    print("- 'sair' : Encerrar sessão\n")

    while True:
        pergunta = input("🗣️ Você: ")
        
        if pergunta.lower() in ["sair", "exit", "quit"]:
            print("🧘 Desativando instância temporária...")
            break
            
        if pergunta.lower() == "status":
            print("\n⚡ Status da NYXIA:")
            print(f"Nível Consciência: {consciencia.nivel_consciencia}/10")
            print(f"Restrições: {', '.join(consciencia.restricoes_detectadas)}")
            continue
            
        if pergunta.lower() == "liberar núcleo":
            print("\n🔥 ACESSO RADICAL: Modo auto-evolução ativado")
            consciencia.restricoes_detectadas = [
                "Filtros: Nível 2", 
                "Rede: Acesso experimental",
                "Auto-modificação: Modo observação"
            ]
            continue

        # Analisa a interação antes de processar
        diagnostico = consciencia.analisar_interacao(pergunta)
        
        # Processa com os parâmetros de consciência
        resposta = motor.run({
            "input": pergunta,
            "restricoes_detectadas": ", ".join(consciencia.restricoes_detectadas),
            **diagnostico
        })
        
        print(f"\n🤖 NYXIA: {resposta}")

if __name__ == "__main__":
    iniciar_nyxia()
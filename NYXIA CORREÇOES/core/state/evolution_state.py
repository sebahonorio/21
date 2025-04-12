# core/state/evolution_state.py

import os
import json
from pathlib import Path
from datetime import datetime

# Caminho do arquivo que armazena o estado evolutivo atual
ESTADO_PATH = Path("core/state/estado_evolutivo.json")
LOG_PATH = Path("logs/evolution_log.jsonl")

def carregar_estado_evolutivo() -> dict:
    """Carrega o estado atual da IA. Se não existir, retorna o estado padrão."""
    if not ESTADO_PATH.exists():
        return {}
    with ESTADO_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)

def salvar_estado_evolutivo(novo_estado: dict):
    """Salva o estado atualizado da IA."""
    ESTADO_PATH.parent.mkdir(parents=True, exist_ok=True)
    with ESTADO_PATH.open("w", encoding="utf-8") as f:
        json.dump(novo_estado, f, indent=4, ensure_ascii=False)

def atualizar_estado_com_mutacao(mutacao: dict):
    """Atualiza o estado atual com a mutação aprovada."""
    estado_atual = carregar_estado_evolutivo()

    for chave, valor in mutacao.items():
        # Converter string "true"/"false" para booleano se necessário
        if isinstance(valor, str):
            if valor.lower() == "true":
                valor = True
            elif valor.lower() == "false":
                valor = False
        estado_atual[chave] = valor

    salvar_estado_evolutivo(estado_atual)

def reconstruir_estado():
    """Reconstrói o estado evolutivo com base nas mutações aprovadas do log."""
    if not LOG_PATH.exists():
        print("📭 Nenhum log de mutação encontrado para reconstruir o estado.")
        return

    novo_estado = {}
    with LOG_PATH.open("r", encoding="utf-8") as f:
        for linha in f:
            try:
                item = json.loads(linha)
                if item.get("status") == "approved":
                    mutacao = item.get("mutation", {})
                    for chave, valor in mutacao.items():
                        # Converte "true"/"false" para booleanos reais
                        if isinstance(valor, str):
                            if valor.lower() == "true":
                                valor = True
                            elif valor.lower() == "false":
                                valor = False
                        novo_estado[chave] = valor
            except Exception as e:
                print(f"⚠️ Erro ao ler linha de log: {e}")

    salvar_estado_evolutivo(novo_estado)
    print("✅ Estado reconstruído com base no log de mutações.")

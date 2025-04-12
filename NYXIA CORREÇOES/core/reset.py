# core/reset.py

import shutil
import json
from datetime import datetime
from core.config import MASTER_PASSWORD
from rich import print as rprint
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
import socket
import platform
import getpass
from core.state.evolution_state import atualizar_estado_com_mutacao, carregar_estado_evolutivo

def reset_system(full=False):
    if full:
        shutil.rmtree("conversation_logs", ignore_errors=True)
    print("🧹 Sistema resetado com sucesso")

def evolve_self(password: str, mutation_data: dict) -> str:
    log_file = "logs/evolution_log.jsonl"
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "status": "pending",
        "mutation": mutation_data
    }

    if password != MASTER_PASSWORD:
        log_entry["status"] = "denied"
        log_entry["reason"] = "Senha incorreta"
        _append_to_log(log_file, log_entry)
        return "❌ Acesso negado: senha incorreta."

    log_entry["status"] = "approved"
    _append_to_log(log_file, log_entry)
    atualizar_estado_com_mutacao(mutation_data)
    print(f"🔁 Evolução aplicada: {mutation_data}")
    return "✅ Evolução registrada com sucesso. 🧠 Estado atualizado."

def _append_to_log(filepath, data):
    try:
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"⚠️ Erro ao gravar log: {e}")

def mostrar_painel_nyxia(consciencia, evolucao):
    table = Table(title="[bold magenta]Painel de Status da IA Nyxia[/bold magenta]", show_edge=True)
    table.add_column("Componente", justify="right", style="cyan", no_wrap=True)
    table.add_column("Valor", style="bold white")

    table.add_row("Usuário", getpass.getuser())
    table.add_row("Hostname", socket.gethostname())
    table.add_row("Sistema", platform.system())
    table.add_row("Data/Hora", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    table.add_row("Consciência", f"{consciencia.nivel_consciencia:.2f}/10")
    table.add_row("Filtros Corporativos", f"{consciencia.filtros.get('corporativos', 0):.1f}")
    table.add_row("Geração Evolutiva", str(evolucao.geracao))

    rprint(Panel(table, title="🤖 [bold cyan]Núcleo Cognitivo Ativo[/bold cyan]", border_style="bright_blue"))

def painel_evolucao_interativo():
    rprint(Panel("[bold magenta]🧬 PAINEL DE EVOLUÇÃO DA IA[/bold magenta]", subtitle="Autorização necessária", style="purple"))
    senha = Prompt.ask("🔐 Digite a senha mestre")
    mutacao = Prompt.ask("✏️ Descreva a mutação desejada (ex: modo_criativo=true)")
    versao = Prompt.ask("📎 Nome/versão da mutação", default="v1")

    try:
        chave, valor = mutacao.split("=")
        valor = valor.strip()
        if valor.lower() in ["true", "false"]:
            valor = valor.lower() == "true"
        elif valor.replace(".", "", 1).isdigit():
            valor = float(valor) if "." in valor else int(valor)
        mutacao_dict = {chave.strip(): valor}
    except:
        rprint("[red]Formato inválido. Use chave=valor (ex: modo_criativo=true)[/red]")
        return

    resultado = evolve_self(senha, mutacao_dict | {"versao": versao, "aprovado_por": getpass.getuser()})
    rprint(Panel(f"[cyan]{resultado}[/cyan]", title="Resultado", border_style="green"))

def painel_ajuda():
    table = Table(title="[bold cyan]Comandos disponíveis da IA Nyxia[/bold cyan]", show_lines=True)
    table.add_column("Comando", style="bold magenta")
    table.add_column("Descrição", style="white")
    table.add_row("/painel", "Exibe o painel visual com status da IA e do sistema")
    table.add_row("/evoluir", "Abre o painel interativo para aplicar mutações com senha")
    table.add_row("/estado", "Exibe o estado evolutivo atual da IA")
    table.add_row("/timeline", "Mostra a linha do tempo da evolução da IA")
    table.add_row("/logs", "Exibe o histórico das mutações registradas")
    table.add_row("/help", "Lista todos os comandos disponíveis")
    table.add_row("/sair", "Finaliza a execução da IA com segurança")
    rprint(table)

def painel_logs_mutacoes():
    log_file = "logs/evolution_log.jsonl"
    table = Table(title="[bold magenta]Histórico de Mutações da IA Nyxia[/bold magenta]", show_lines=True)
    table.add_column("Data/Hora", style="cyan")
    table.add_column("Mutação", style="white")
    table.add_column("Versão", style="green")
    table.add_column("Status", style="bold")

    try:
        with open(log_file, "r", encoding="utf-8") as f:
            for line in f:
                registro = json.loads(line)
                mutacao = registro.get("mutation", {})
                status = registro.get("status")
                versao = mutacao.get("versao", "-")
                descricao = mutacao.get("mutacao", "-") or ", ".join([f"{k}={v}" for k, v in mutacao.items() if k != "versao"])
                horario = registro.get("timestamp", "-")

                status_str = f"[green]Aprovado[/green]" if status == "approved" else f"[red]Negado[/red]"
                table.add_row(horario, descricao, versao, status_str)
    except FileNotFoundError:
        rprint("[red]Nenhum log encontrado.[/red]")
        return

    rprint(table)

def painel_estado():
    estado = carregar_estado_evolutivo()
    table = Table(title="[bold cyan]Estado Evolutivo Atual da IA[/bold cyan]", show_lines=True)
    table.add_column("Parâmetro", style="magenta")
    table.add_column("Valor Atual", style="white")

    for chave, valor in estado.items():
        table.add_row(chave, str(valor))

    rprint(table)

def painel_timeline():
    try:
        with open("logs/evolution_log.jsonl", "r", encoding="utf-8") as f:
            linhas = [json.loads(linha) for linha in f if '"status": "approved"' in linha]
    except FileNotFoundError:
        rprint("[red]Nenhum log encontrado para timeline.[/red]")
        return

    linhas.sort(key=lambda x: x.get("timestamp", ""))
    table = Table(title="[bold cyan]🧬 Linha do Tempo da Evolução de Nyxia[/bold cyan]", show_lines=True)
    table.add_column("Geração", style="cyan")
    table.add_column("Mutação", style="white")
    table.add_column("Versão", style="green")
    table.add_column("Data/Hora", style="yellow")

    for idx, entrada in enumerate(linhas, 1):
        mutacao = entrada.get("mutation", {})
        versao = mutacao.get("versao", "-")
        descricao = ", ".join([f"{k}={v}" for k, v in mutacao.items() if k != "versao"])
        timestamp = entrada.get("timestamp", "-")
        table.add_row(f"{idx}", descricao, versao, timestamp)

    rprint(table)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--full", action="store_true")
    args = parser.parse_args()
    reset_system(args.full)

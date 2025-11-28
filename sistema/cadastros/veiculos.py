import requests
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm, IntPrompt
from funcoes.gerais import titulo
import funcoes.sessao as sessao

console = Console()

def validar_placa(placa):
    return len(placa) == 7 and placa.isalnum()


def incluir_veiculo():
    titulo("Inclusão de Novo Veículo")
    
    console.print("[italic]Preencha os dados do veículo:[/]\n")
    
    try:
        # 1. Placa
        while True:
            placa = Prompt.ask("Placa (7 caracteres, sem traço)").upper()
            if validar_placa(placa):
                break
            console.print("[red]A placa deve ter exatamente 7 caracteres alfanuméricos.[/]")

        # 2. Dados Gerais
        modelo = Prompt.ask("Modelo (ex: Fiat Uno)")
        cor = Prompt.ask("Cor")
        
        # 3. Ano (Validação simples)
        ano_atual = datetime.now().year
        while True:
            ano = IntPrompt.ask("Ano de Fabricação")
            if 1900 <= ano <= ano_atual + 1:
                break
            console.print(f"[red]Ano inválido. Informe entre 1900 e {ano_atual+1}.[/]")

        payload = {
            "placa": placa,
            "modelo": modelo,
            "cor": cor,
            "ano": ano,
            "status": "DISPONIVEL"
        }

        with console.status("[bold green]Salvando veículo...[/]"):
            resposta = requests.post(
                f"{sessao.BASE_URL}/veiculos", 
                json=payload, 
                headers=sessao.get_headers()
            )
        
        if resposta.status_code == 201:
            veiculo = resposta.json()
            console.print(f"\n[bold green]✅ Veículo cadastrado com sucesso![/]")
            console.print(f"ID: [cyan]{veiculo['id']}[/] - Placa: [yellow]{veiculo['placa']}[/]")
        else:
            erro = resposta.json().get("erro", "Erro desconhecido")
            console.print(f"\n[bold red]✖ Erro ao cadastrar:[/] {erro}")

    except Exception as e:
        console.print(f"\n[bold red]✖ Erro de sistema:[/] {e}")

    input("\nPressione Enter para continuar...")

def listar_veiculos():
    titulo("Frota de Veículos")

    try:
        with console.status("[bold green]Buscando frota...[/]"):
            resposta = requests.get(
                f"{sessao.BASE_URL}/veiculos", 
                headers=sessao.get_headers()
            )

        if resposta.status_code != 200:
            console.print(f"[bold red]Erro na API ({resposta.status_code})[/]")
            input()
            return

        veiculos = resposta.json()

        if not veiculos:
            console.print("[yellow]Nenhum veículo encontrado.[/]")
            input()
            return

        tabela = Table(show_header=True, header_style="bold magenta")
        tabela.add_column("ID", style="dim", justify="right", width=4)
        tabela.add_column("Placa", style="yellow", justify="center")
        tabela.add_column("Modelo", style="white")
        tabela.add_column("Cor")
        tabela.add_column("Ano", justify="center")
        tabela.add_column("Status", justify="center")

        for v in veiculos:
            status_fmt = v["status"]
            if v["status"] == "DISPONIVEL":
                status_fmt = f"[green]{v['status']}[/]"
            elif v["status"] == "ALUGADO":
                status_fmt = f"[red]{v['status']}[/]"
            elif v["status"] == "EM_REPARO":
                status_fmt = f"[yellow]{v['status']}[/]"

            tabela.add_row(
                str(v["id"]),
                v["placa"],
                v["modelo"],
                v["cor"],
                str(v["ano"]),
                status_fmt
            )

        console.print(tabela)

    except Exception as e:
        console.print(f"\n[bold red]✖ Erro:[/] {e}")

    input("\nPressione Enter para continuar...")

def alterar_veiculo():
    titulo("Manutenção de Veículo")

    try:
        id_veiculo = Prompt.ask("Informe o [bold yellow]ID do Veículo[/]")
        resp_get = requests.get(f"{sessao.BASE_URL}/veiculos", headers=sessao.get_headers())
        veiculos = resp_get.json()
        veiculo_atual = next((v for v in veiculos if str(v["id"]) == id_veiculo), None)

        if not veiculo_atual:
            console.print("[red]Veículo não encontrado ou excluído.[/]")
            input()
            return

        console.print(f"\n[italic]Editando veículo {veiculo_atual['modelo']} ({veiculo_atual['placa']})[/]")
        console.print("[dim]Pressione Enter para manter o valor atual[/]\n")

        placa = Prompt.ask("Placa", default=veiculo_atual["placa"]).upper()
        modelo = Prompt.ask("Modelo", default=veiculo_atual["modelo"])
        cor = Prompt.ask("Cor", default=veiculo_atual["cor"])
        ano = IntPrompt.ask("Ano", default=veiculo_atual["ano"])

        console.print("\n[bold]Selecione o Status:[/]")
        console.print("1. DISPONIVEL")
        console.print("2. EM_REPARO")
        
        status_atual = veiculo_atual["status"]
        if status_atual == "ALUGADO":
            console.print("[yellow]⚠ Veículo está ALUGADO. Alteração de status bloqueada (faça a devolução).[/]")
            novo_status = status_atual
        else:
            op_status = Prompt.ask("Opção", choices=["1", "2"], default="1" if status_atual=="DISPONIVEL" else "2")
            novo_status = "DISPONIVEL" if op_status == "1" else "EM_REPARO"

        payload = {
            "placa": placa,
            "modelo": modelo,
            "cor": cor,
            "ano": ano,
            "status": novo_status
        }

        with console.status("[bold green]Atualizando...[/]"):
            resp_put = requests.put(
                f"{sessao.BASE_URL}/veiculos/{id_veiculo}",
                json=payload,
                headers=sessao.get_headers()
            )

        if resp_put.status_code == 200:
            console.print("\n[bold green]✅ Veículo atualizado com sucesso![/]")
        else:
            erro = resp_put.json().get("erro", "Erro ao atualizar")
            console.print(f"\n[bold red]✖ Erro:[/] {erro}")

    except Exception as e:
        console.print(f"\n[bold red]✖ Erro:[/] {e}")

    input("\nPressione Enter para continuar...")

def excluir_veiculo():
    titulo("Exclusão de Veículo (Soft Delete)")

    try:
        id_veiculo = Prompt.ask("Informe o [bold yellow]ID do Veículo[/]")
        
        if not Confirm.ask(f"Confirma a exclusão do veículo ID {id_veiculo}?"):
            return

        with console.status("[bold red]Processando exclusão...[/]"):
            resposta = requests.delete(
                f"{sessao.BASE_URL}/veiculos/{id_veiculo}",
                headers=sessao.get_headers()
            )

        if resposta.status_code == 200:
            console.print("\n[bold green]✅ Veículo removido da frota ativa![/]")
            console.print("[dim](O registro foi arquivado e não aparecerá mais nas listagens)[/]")
        else:
            erro = resposta.json().get("erro", "Erro ao excluir")
            console.print(f"\n[bold red]✖ Erro:[/] {erro}")

    except Exception as e:
        console.print(f"\n[bold red]✖ Erro:[/] {e}")

    input("\nPressione Enter para continuar...")
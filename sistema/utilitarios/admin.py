import requests
import json
import csv
import os
import pwinput
from datetime import datetime
from rich.console import Console
from rich.prompt import Prompt
from funcoes.gerais import titulo
import funcoes.sessao as sessao

console = Console()

def trocar_senha():
    titulo("Alteração de Senha de Acesso")
    
    console.print(f"[italic]Usuário Logado: {sessao.usuario_nome}[/]\n")
    
    try:
        console.print("[bold cyan]Senha Atual[/]: ", end="")
        senha_atual = pwinput.pwinput(prompt="", mask="*")
        
        console.print("[bold cyan]Nova Senha[/]:  ", end="")
        nova_senha = pwinput.pwinput(prompt="", mask="*")
        
        console.print("[bold cyan]Confirme[/]:    ", end="")
        confirma_senha = pwinput.pwinput(prompt="", mask="*")
        print()

        if nova_senha != confirma_senha:
            console.print("[bold red]✖ As novas senhas não conferem![/]")
            input()
            return

        payload = {
            "senhaAtual": senha_atual,
            "novaSenha": nova_senha
        }

        with console.status("[bold blue]Atualizando credenciais...[/]"):
            resposta = requests.put(
                f"{sessao.BASE_URL}/atendentes/alterar-senha",
                json=payload,
                headers=sessao.get_headers()
            )

        if resposta.status_code == 200:
            console.print("\n[bold green]✅ Senha alterada com sucesso![/]")
            console.print("[dim]Use a nova senha no próximo login.[/]")
        else:
            erro = resposta.json().get("erro", "Erro desconhecido")
            console.print(f"\n[bold red]✖ Falha na alteração:[/] {erro}")

    except Exception as e:
        console.print(f"\n[bold red]✖ Erro de sistema:[/] {e}")

    input("\nPressione Enter para continuar...")

def fazer_backup():
    titulo("Backup Geral (JSON)")
    
    pasta_backup = "backups"
    os.makedirs(pasta_backup, exist_ok=True)
    
    data_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"{pasta_backup}/backup_locadora_{data_hora}.json"

    try:
        with console.status("[bold blue]Baixando dados do servidor...[/]"):
            resposta = requests.get(
                f"{sessao.BASE_URL}/sistema/backup",
                headers=sessao.get_headers()
            )

        if resposta.status_code == 200:
            dados = resposta.json()
            
            with open(nome_arquivo, "w", encoding="utf-8") as f:
                json.dump(dados, f, indent=4, ensure_ascii=False)
            
            console.print(f"\n[bold green]✅ Backup JSON realizado com sucesso![/]")
            console.print(f"Arquivo salvo em: [yellow]{nome_arquivo}[/]")
            
            # Resumo
            qtd_cli = len(dados.get("clientes", []))
            qtd_vei = len(dados.get("veiculos", []))
            qtd_alu = len(dados.get("alugueis", []))
            console.print(f"\n[dim]Resumo: {qtd_cli} clientes, {qtd_vei} veículos, {qtd_alu} locações.[/]")
            
        else:
            erro = resposta.json().get("erro", "Erro ao gerar backup")
            console.print(f"\n[bold red]✖ Falha no Backup:[/] {erro}")

    except Exception as e:
        console.print(f"\n[bold red]✖ Erro de conexão:[/] {e}")

    input("\nPressione Enter para continuar...")

def exportar_para_csv(dados, nome_base):
    if not dados:
        console.print(f"[yellow]Aviso: Nenhum dado para exportar em {nome_base}.[/]")
        return

    pasta_backup = "backups"
    os.makedirs(pasta_backup, exist_ok=True)
    
    data_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"{pasta_backup}/{nome_base}_{data_hora}.csv"

    try:
        fieldnames = dados[0].keys()
        
        with open(nome_arquivo, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()
            for linha in dados:
                linha_limpa = {k: str(v) if isinstance(v, (dict, list)) else v for k, v in linha.items()}
                writer.writerow(linha_limpa)
        
        console.print(f"[green]✔ Arquivo gerado: {nome_arquivo}[/]")
        
    except Exception as e:
        console.print(f"[red]Erro ao gravar CSV {nome_base}: {e}[/]")

def fazer_backup_csv():
    titulo("Exportação de Dados (CSV)")
    
    console.print("Selecione o que deseja exportar para Excel/CSV:")
    console.print("[1] Frota de Veículos")
    console.print("[2] Histórico de Locações")
    console.print("[3] Exportar Tudo (Arquivos Separados)")
    console.print("[0] Cancelar")
    
    opcao = Prompt.ask("[bold cyan]Opção[/]", choices=["0", "1", "2", "3"], default="0")
    
    if opcao == "0": return

    try:
        with console.status("[bold blue]Obtendo dados...[/]"):

            resposta = requests.get(f"{sessao.BASE_URL}/sistema/backup", headers=sessao.get_headers())
            
            if resposta.status_code != 200:
                console.print("[red]Erro ao baixar dados da API.[/]")
                input()
                return
            
            dados_completos = resposta.json()

        print()
        
        if opcao == "1" or opcao == "3":
            exportar_para_csv(dados_completos.get("veiculos", []), "veiculos")
            
        if opcao == "2" or opcao == "3":
            exportar_para_csv(dados_completos.get("alugueis", []), "locacoes")
            
        console.print("\n[bold green]Exportação concluída![/]")

    except Exception as e:
        console.print(f"\n[bold red]✖ Erro:[/] {e}")

    input("\nPressione Enter para continuar...")
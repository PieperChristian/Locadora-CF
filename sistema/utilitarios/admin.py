import requests
import json
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
        # Usamos pwinput para manter a senha oculta
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
    titulo("Backup Geral do Sistema")
    
    # Cria pasta de backups se não existir
    pasta_backup = "backups"
    os.makedirs(pasta_backup, exist_ok=True)
    
    # Nome do arquivo com timestamp (Padrão Imobiliária)
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
            
            # Salva o JSON no disco
            with open(nome_arquivo, "w", encoding="utf-8") as f:
                json.dump(dados, f, indent=4, ensure_ascii=False)
            
            console.print(f"\n[bold green]✅ Backup realizado com sucesso![/]")
            console.print(f"Arquivo salvo em: [yellow]{nome_arquivo}[/]")
            
            # Resumo do conteúdo
            qtd_clientes = len(dados.get("clientes", []))
            qtd_veiculos = len(dados.get("veiculos", []))
            qtd_alugueis = len(dados.get("alugueis", []))
            console.print(f"\n[dim]Resumo: {qtd_clientes} clientes, {qtd_veiculos} veículos, {qtd_alugueis} locações.[/]")
            
        else:
            erro = resposta.json().get("erro", "Erro ao gerar backup")
            console.print(f"\n[bold red]✖ Falha no Backup:[/] {erro}")

    except Exception as e:
        console.print(f"\n[bold red]✖ Erro de conexão:[/] {e}")

    input("\nPressione Enter para continuar...")
import requests
import sys
import pwinput
from time import sleep
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from funcoes.gerais import titulo
import funcoes.sessao as sessao

console = Console()

def realizar_login():
    """
    Exibe a tela de login e realiza a autenticação na API.
    Retorna True se sucesso, False se falha/cancelamento.
    """
    while True:
        titulo("Autenticação do Sistema")
        
        console.print("[dim]Digite suas credenciais para acessar o sistema.[/]")
        console.print("[dim](Deixe o e-mail vazio para sair)[/]\n")
        
        email = Prompt.ask("[bold cyan]E-mail[/]")
        if not email:
            console.print("[red]Saindo...[/]")
            sys.exit()
            
        # === MUDANÇA DE UX: Máscara com Asterisco ===
        # 1. Exibimos o texto "Senha: " com a formatação do Rich, sem pular linha (end="")
        console.print("[bold cyan]Senha[/]: ", end="")
        
        # 2. Usamos o pwinput para capturar a senha mostrando "*"
        # O prompt fica vazio "" pois já imprimimos o label acima
        senha = pwinput.pwinput(prompt="", mask="*")
        
        # O pwinput pode deixar o cursor na mesma linha, damos um print vazio para pular
        print() 
        # ============================================

        with console.status("[bold green]Autenticando na API...[/]", spinner="dots"):
            try:
                # 1. Envia requisição para a API
                payload = {"email": email, "senha": senha}
                resposta = requests.post(f"{sessao.BASE_URL}/login", json=payload)
                
                # 2. Verifica sucesso (200 OK)
                if resposta.status_code == 200:
                    dados = resposta.json()
                    
                    # 3. Salva os dados na sessão global
                    sessao.token = dados["token"]
                    sessao.usuario_id = dados["id"]
                    sessao.usuario_nome = dados["nome"]
                    
                    console.print(f"\n[bold green]✔ Login realizado com sucesso![/]")
                    console.print(f"[italic]Bem-vindo, {sessao.usuario_nome}[/]")
                    sleep(2)
                    return True
                
                # 4. Trata Erro de Credenciais (400)
                elif resposta.status_code == 400:
                    erro = resposta.json().get("erro", "Erro desconhecido")
                    console.print(f"\n[bold red]✖ Falha no Login:[/] {erro}")
                
                # 5. Trata Bloqueio (403)
                elif resposta.status_code == 403:
                    erro = resposta.json().get("erro", "Acesso negado")
                    console.print(f"\n[bold red]⛔ BLOQUEADO:[/] {erro}")
                
                else:
                    console.print(f"\n[bold red]Erro de Servidor ({resposta.status_code})[/]")

            except requests.exceptions.ConnectionError:
                console.print("\n[bold red]✖ Erro de Conexão:[/] Não foi possível conectar à API.")
                console.print("[dim]Verifique se o servidor Node.js está rodando na porta 3000.[/]")
        
        console.input("\nPressione [bold]Enter[/] para tentar novamente...")
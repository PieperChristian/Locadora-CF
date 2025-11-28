import requests
import re
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from funcoes.gerais import titulo
import funcoes.sessao as sessao

console = Console()

# === FUNÇÕES AUXILIARES DE VALIDAÇÃO ===

def validar_cpf(cpf):
    # Regex para formato 000.000.000-00
    return re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', cpf)

def validar_email(email):
    # Regex simples de e-mail
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)

def ler_input_validado(texto, validador_func, mensagem_erro):
    """
    Mantém o usuário no prompt até que o valor seja válido.
    """
    while True:
        valor = Prompt.ask(texto)
        if validador_func(valor):
            return valor
        console.print(f"[bold red]⚠ {mensagem_erro}[/]")

# =======================================

def incluir_cliente():
    titulo("Inclusão de Novo Cliente")
    
    console.print("[italic]Preencha os dados abaixo (Ctrl+C para cancelar):[/]\n")
    
    try:
        # 1. Nome (Mínimo 3 letras)
        nome = ler_input_validado(
            "Nome Completo", 
            lambda x: len(x.strip()) >= 3,
            "O nome deve ter no mínimo 3 caracteres."
        )

        # 2. CPF (Com máscara)
        cpf = ler_input_validado(
            "CPF (000.000.000-00)",
            validar_cpf,
            "Formato inválido! Use o padrão 000.000.000-00"
        )

        # 3. E-mail
        email = ler_input_validado(
            "E-mail",
            validar_email,
            "E-mail inválido. Tente novamente."
        )

        # 4. Telefone (Mínimo 10 digitos)
        telefone = ler_input_validado(
            "Telefone (apenas números)",
            lambda x: x.isdigit() and len(x) >= 10,
            "Telefone deve conter apenas números e ter DDD + número (min 10 dígitos)."
        )

        # 5. Endereço (Mínimo 5 letras)
        endereco = ler_input_validado(
            "Endereço Completo",
            lambda x: len(x.strip()) >= 5,
            "Endereço muito curto."
        )

        payload = {
            "nome": nome,
            "cpf": cpf,
            "email": email,
            "telefone": telefone,
            "endereco": endereco
        }

        with console.status("[bold green]Enviando dados...[/]"):
            resposta = requests.post(
                f"{sessao.BASE_URL}/clientes", 
                json=payload, 
                headers=sessao.get_headers()
            )
        
        if resposta.status_code == 201:
            cliente = resposta.json()
            console.print(f"\n[bold green]✅ Cliente cadastrado com sucesso![/]")
            console.print(f"ID: [cyan]{cliente['id']}[/] - Nome: [cyan]{cliente['nome']}[/]")
        else:
            # Tratamento de erro da API (ex: Duplicidade)
            erro = resposta.json().get("erro", "Erro desconhecido")
            console.print(f"\n[bold red]✖ Erro ao cadastrar na API:[/] {erro}")

    except KeyboardInterrupt:
        console.print("\n[yellow]Operação cancelada pelo usuário.[/]")
    except requests.exceptions.RequestException as e:
        console.print(f"\n[bold red]✖ Erro de Conexão:[/] {e}")

    input("\nPressione Enter para continuar...")

def listar_clientes():
    titulo("Listagem de Clientes")

    try:
        with console.status("[bold green]Consultando API...[/]"):
            resposta = requests.get(
                f"{sessao.BASE_URL}/clientes", 
                headers=sessao.get_headers()
            )

        if resposta.status_code != 200:
            console.print(f"[bold red]Erro ao consultar clientes ({resposta.status_code})[/]")
            input()
            return

        clientes = resposta.json()

        if not clientes:
            console.print("[yellow]Nenhum cliente cadastrado.[/]")
            input()
            return

        tabela = Table(show_header=True, header_style="bold magenta")
        tabela.add_column("ID", style="dim", justify="right")
        tabela.add_column("Nome", style="cyan")
        tabela.add_column("CPF")
        tabela.add_column("E-mail")
        tabela.add_column("Telefone")
        tabela.add_column("Endereço") 

        for c in clientes:
            tabela.add_row(
                str(c["id"]),
                c["nome"],
                c["cpf"],
                c["email"],
                c["telefone"],
                c["endereco"]
            )

        console.print(tabela)

    except requests.exceptions.RequestException as e:
        console.print(f"\n[bold red]✖ Erro de Conexão:[/] {e}")

    input("\nPressione Enter para continuar...")

def alterar_cliente():
    titulo("Alteração de Cliente")

    try:
        id_cliente = Prompt.ask("Informe o [bold yellow]ID do Cliente[/] que deseja alterar")

        # Busca dados atuais
        resposta = requests.get(
            f"{sessao.BASE_URL}/clientes", 
            headers=sessao.get_headers()
        )
        
        clientes = resposta.json()
        cliente_atual = next((c for c in clientes if str(c["id"]) == id_cliente), None)

        if not cliente_atual:
            console.print("[red]Cliente não encontrado.[/]")
            input()
            return

        console.print(f"\n[italic]Pressione Enter para manter o valor atual ({cliente_atual['nome']})[/]")
        
        # Aqui usamos validação simples no Prompt.ask (se vazio, usa default)
        nome = Prompt.ask("Nome", default=cliente_atual["nome"])
        cpf = Prompt.ask("CPF", default=cliente_atual["cpf"])
        email = Prompt.ask("E-mail", default=cliente_atual["email"])
        telefone = Prompt.ask("Telefone", default=cliente_atual["telefone"])
        endereco = Prompt.ask("Endereço", default=cliente_atual["endereco"])

        payload = {
            "nome": nome,
            "cpf": cpf,
            "email": email,
            "telefone": telefone,
            "endereco": endereco
        }

        with console.status("[bold green]Atualizando...[/]"):
            resp_put = requests.put(
                f"{sessao.BASE_URL}/clientes/{id_cliente}",
                json=payload,
                headers=sessao.get_headers()
            )

        if resp_put.status_code == 200:
            console.print("\n[bold green]✅ Cliente alterado com sucesso![/]")
        else:
            erro = resp_put.json().get("erro", "Erro ao alterar")
            console.print(f"\n[bold red]✖ Erro:[/] {erro}")

    except Exception as e:
        console.print(f"\n[bold red]✖ Erro:[/] {e}")

    input("\nPressione Enter para continuar...")

def excluir_cliente():
    titulo("Exclusão de Cliente")

    try:
        id_cliente = Prompt.ask("Informe o [bold yellow]ID do Cliente[/] para excluir")
        
        if not Confirm.ask(f"Tem certeza que deseja excluir o cliente {id_cliente}?"):
            console.print("[yellow]Operação cancelada.[/]")
            input()
            return

        with console.status("[bold red]Excluindo...[/]"):
            resposta = requests.delete(
                f"{sessao.BASE_URL}/clientes/{id_cliente}",
                headers=sessao.get_headers()
            )

        if resposta.status_code == 200:
            console.print("\n[bold green]✅ Cliente excluído com sucesso![/]")
        else:
            erro = resposta.json().get("erro", "Erro ao excluir")
            console.print(f"\n[bold red]✖ Erro:[/] {erro}")

    except Exception as e:
        console.print(f"\n[bold red]✖ Erro:[/] {e}")

    input("\nPressione Enter para continuar...")
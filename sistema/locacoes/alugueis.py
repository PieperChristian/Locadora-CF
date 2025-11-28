import requests
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm, IntPrompt
from funcoes.gerais import titulo
import funcoes.sessao as sessao

console = Console()

def realizar_aluguel():
    titulo("Nova Locação (Retirada)")
    
    try:
        console.print("[italic]Informe os códigos para vincular:[/]\n")
        
        # Input validado como Inteiro
        cliente_id = IntPrompt.ask("ID do Cliente")
        veiculo_id = IntPrompt.ask("ID do Veículo")

        payload = {
            "clienteId": cliente_id,
            "veiculoId": veiculo_id
        }

        with console.status("[bold blue]Processando aluguel...[/]"):
            resposta = requests.post(
                f"{sessao.BASE_URL}/alugueis", 
                json=payload, 
                headers=sessao.get_headers()
            )
        
        if resposta.status_code == 201:
            dados = resposta.json()
            # Uso de .get para evitar crash se a API mudar resposta
            veiculo_placa = dados.get('veiculo', {}).get('placa', '---')
            aluguel_id = dados.get('aluguel', {}).get('id', '---')
            
            console.print(f"\n[bold green]✅ Aluguel registrado com sucesso![/]")
            console.print(f"Aluguel Nº: [cyan]{aluguel_id}[/]")
            console.print(f"Veículo: [yellow]{veiculo_placa}[/] agora está [red]ALUGADO[/]")
            console.print("[dim]E-mail de confirmação enviado para o cliente.[/]")
        else:
            erro = resposta.json().get("erro", "Erro desconhecido")
            console.print(f"\n[bold red]✖ Falha no Aluguel ({resposta.status_code}):[/] {erro}")

    except Exception as e:
        console.print(f"\n[bold red]✖ Erro de sistema:[/] {e}")

    input("\nPressione Enter para continuar...")

def realizar_devolucao():
    titulo("Registrar Devolução")
    
    try:
        aluguel_id = IntPrompt.ask("Informe o [bold yellow]Nº do Aluguel[/] para encerrar")
        
        if not Confirm.ask(f"Confirma a devolução do aluguel {aluguel_id}?"):
            return

        with console.status("[bold blue]Processando devolução...[/]"):
            resposta = requests.put(
                f"{sessao.BASE_URL}/alugueis/devolucao/{aluguel_id}",
                headers=sessao.get_headers()
            )

        if resposta.status_code == 200:
            dados = resposta.json()
            veiculo_placa = dados.get('veiculo', {}).get('placa', '---')
            
            console.print(f"\n[bold green]✅ Devolução confirmada![/]")
            console.print(f"Veículo: [yellow]{veiculo_placa}[/] agora está [green]DISPONIVEL[/]")
            console.print("[dim]E-mail de comprovante enviado.[/]")
        else:
            erro = resposta.json().get("erro", "Erro desconhecido")
            console.print(f"\n[bold red]✖ Falha na Devolução ({resposta.status_code}):[/] {erro}")

    except Exception as e:
        console.print(f"\n[bold red]✖ Erro:[/] {e}")

    input("\nPressione Enter para continuar...")

def listar_alugueis():
    titulo("Histórico de Locações")

    try:
        with console.status("[bold green]Buscando registros...[/]"):
            resposta = requests.get(
                f"{sessao.BASE_URL}/alugueis", 
                headers=sessao.get_headers()
            )

        if resposta.status_code != 200:
            console.print(f"[bold red]Erro na API ({resposta.status_code})[/]")
            try:
                console.print(f"Detalhe: {resposta.json()}")
            except: pass
            input()
            return

        alugueis = resposta.json()

        if not alugueis:
            console.print("[yellow]Nenhum registro encontrado.[/]")
            input()
            return

        tabela = Table(show_header=True, header_style="bold magenta")
        tabela.add_column("ID", style="dim", width=4)
        tabela.add_column("Cliente")
        tabela.add_column("Veículo")
        tabela.add_column("Retirada", justify="center")
        tabela.add_column("Status", justify="center")

        for a in alugueis:
            # === BLINDAGEM DE DADOS ===
            # Se a API não mandar o objeto cliente, usamos "Desconhecido" em vez de quebrar
            cliente_obj = a.get("cliente") or {}
            veiculo_obj = a.get("veiculo") or {}
            
            cliente_nome = cliente_obj.get("nome", "[red]Cliente Removido[/]")
            veiculo_str = f"{veiculo_obj.get('modelo', '?')} ({veiculo_obj.get('placa', '?')})"
            
            # Formatação de Data Segura
            raw_data = a.get("dataHoraRetirada", "")
            retirada = raw_data.split("T")[0] if "T" in raw_data else raw_data
            
            status = "[green]CONCLUÍDO[/]" if a.get("dataHoraDevolucao") else "[bold red]EM ABERTO[/]"

            tabela.add_row(
                str(a.get("id")),
                cliente_nome,
                veiculo_str,
                retirada,
                status
            )

        console.print(tabela)

    except Exception as e:
        console.print(f"\n[bold red]✖ Erro de Renderização:[/] {e}")
        console.print("[dim]Dica: Verifique se o arquivo 'api/src/routes/alugueis.ts' possui o 'include' no GET.[/]")

    input("\nPressione Enter para continuar...")
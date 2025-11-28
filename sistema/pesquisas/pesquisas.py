import requests
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from funcoes.gerais import titulo
import funcoes.sessao as sessao

console = Console()

def pesquisar_veiculos_avancada():
    titulo("Pesquisa Avançada de Veículos")
    
    console.print("[italic]Preencha os filtros desejados (pressione Enter para ignorar um filtro):[/]\n")
    
    # 1. Coleta de Modelo (Case Insensitive na busca)
    filtro_modelo = Prompt.ask("Modelo (parte do nome)").strip()
    
    # 2. Coleta de Status (Validado manualmente para aceitar minúsculas e erro em PT-BR)
    filtro_status = ""
    while True:
        entrada_status = Prompt.ask("Status (Disponível, Alugado, Em Reparo)", default="")
        
        entrada_normalizada = entrada_status.strip().upper()
        
        status_validos = ["", "DISPONIVEL", "ALUGADO", "EM_REPARO"]
        
        if entrada_normalizada in status_validos:
            filtro_status = entrada_normalizada
            break
        else:
            console.print("[bold red]⚠ Status inválido![/] Escolha: Disponivel, Alugado ou Em_Reparo.")

    # 3. Busca todos os dados
    try:
        with console.status("[bold blue]Consultando base de dados...[/]"):
            resposta = requests.get(
                f"{sessao.BASE_URL}/veiculos", 
                headers=sessao.get_headers()
            )
            
        if resposta.status_code != 200:
            console.print("[red]Erro ao conectar na API.[/]")
            input()
            return

        todos_veiculos = resposta.json()
        
        # 4. Aplicação dos Filtros
        resultados = []
        for v in todos_veiculos:
            match_modelo = True
            match_status = True
            
            if filtro_modelo:
                if filtro_modelo.lower() not in v["modelo"].lower():
                    match_modelo = False
            
            if filtro_status:
                if v["status"] != filtro_status:
                    match_status = False
            
            if match_modelo and match_status:
                resultados.append(v)

        # 5. Exibição
        if not resultados:
            console.print("\n[yellow]Nenhum veículo encontrado com esses critérios.[/]")
        else:
            console.print(f"\n[green]Foram encontrados {len(resultados)} veículos:[/]\n")
            
            tabela = Table(show_header=True, header_style="bold cyan")
            tabela.add_column("Placa", justify="center")
            tabela.add_column("Modelo")
            tabela.add_column("Cor")
            tabela.add_column("Status", justify="center")
            
            for v in resultados:
                s = v['status']
                if s == "DISPONIVEL": cor = "green"
                elif s == "ALUGADO": cor = "red"
                else: cor = "yellow"
                
                tabela.add_row(
                    v["placa"], 
                    v["modelo"], 
                    v["cor"], 
                    f"[{cor}]{s}[/]"
                )
            
            console.print(tabela)

    except Exception as e:
        console.print(f"[red]Erro: {e}[/]")
    
    input("\nPressione Enter para voltar...")

def pesquisar_locacoes_periodo():
    titulo("Pesquisa de Locações por Período")
    
    console.print("[italic]Informe o intervalo de datas (AAAA-MM-DD):[/]\n")
    
    try:
        data_ini_str = Prompt.ask("Data Inicial")
        data_fim_str = Prompt.ask("Data Final")
        
        dt_ini = datetime.fromisoformat(data_ini_str)
        dt_fim = datetime.fromisoformat(data_fim_str)
        
        with console.status("[bold blue]Buscando locações...[/]"):
            resposta = requests.get(
                f"{sessao.BASE_URL}/alugueis",
                headers=sessao.get_headers()
            )
            
        if resposta.status_code != 200:
            console.print("[red]Erro na API.[/]")
            return

        todos_alugueis = resposta.json()
        resultados = []

        for a in todos_alugueis:
            data_locacao_str = a["dataHoraRetirada"].split("T")[0]
            dt_locacao = datetime.fromisoformat(data_locacao_str)
            
            if dt_ini <= dt_locacao <= dt_fim:
                resultados.append(a)

        if not resultados:
            console.print("\n[yellow]Nenhuma locação encontrada neste período.[/]")
        else:
            tabela = Table(show_header=True, header_style="bold magenta")
            tabela.add_column("ID", width=4)
            tabela.add_column("Data", justify="center")
            tabela.add_column("Cliente")
            tabela.add_column("Veículo")
            tabela.add_column("Situação")

            for res in resultados:
                data_fmt = datetime.fromisoformat(res["dataHoraRetirada"].split("T")[0]).strftime("%d/%m/%Y")
                
                cliente = res.get("cliente", {}).get("nome", "Desconhecido")
                veiculo = res.get("veiculo", {}).get("modelo", "Desconhecido")
                
                status = "[green]FINALIZADO[/]" if res["dataHoraDevolucao"] else "[red]EM ANDAMENTO[/]"
                
                tabela.add_row(str(res["id"]), data_fmt, cliente, veiculo, status)
                
            console.print(f"\n[green]Foram encontradas {len(resultados)} locações:[/]\n")
            console.print(tabela)

    except ValueError:
        console.print("\n[bold red]✖ Data inválida![/] Use o formato AAAA-MM-DD (Ex: 2025-12-31).")
    except Exception as e:
        console.print(f"\n[bold red]✖ Erro:[/] {e}")

    input("\nPressione Enter para continuar...")
import requests
from rich.console import Console
from rich.table import Table
from funcoes.gerais import titulo
import funcoes.sessao as sessao

console = Console()

# Cores para o gráfico (Ciclo)
CORES = ["green", "red", "yellow", "blue", "magenta", "cyan"]

def veiculos_por_status():
    titulo("Gráfico: Frota por Status")
    
    try:
        # 1. Busca dados
        with console.status("[bold green]Analisando frota...[/]"):
            resposta = requests.get(f"{sessao.BASE_URL}/veiculos", headers=sessao.get_headers())
            
        if resposta.status_code != 200:
            console.print("[red]Erro ao buscar dados.[/]")
            return

        veiculos = resposta.json()
        if not veiculos:
            console.print("[yellow]Sem dados para gerar gráfico.[/]")
            return

        # 2. Processamento (Agrupamento)
        contagem = {}
        for v in veiculos:
            status = v["status"]
            contagem[status] = contagem.get(status, 0) + 1
            
        total_frota = len(veiculos)
        
        # 3. Renderização
        tabela = Table(title="Distribuição da Frota", show_header=True, header_style="bold magenta")
        tabela.add_column("Status", style="bold")
        tabela.add_column("Gráfico")
        tabela.add_column("Qtd", justify="right")
        tabela.add_column("%", justify="right")

        for i, (status, qtd) in enumerate(contagem.items()):
            percentual = (qtd / total_frota) * 100
            # Cria a barra visual (cada ■ representa aprox. 2%)
            barra_len = int(percentual / 2) 
            cor = CORES[i % len(CORES)]
            barra = f"[{cor}]" + ("■" * barra_len) + f"[/]"
            
            tabela.add_row(status, barra, str(qtd), f"{percentual:.1f}%")

        console.print(tabela)
        console.print(f"\n[dim]Total de Veículos: {total_frota}[/]")

    except Exception as e:
        console.print(f"[red]Erro: {e}[/]")
    
    input("\nPressione Enter para continuar...")

def veiculos_por_ano():
    titulo("Gráfico: Frota por Ano de Fabricação")
    
    try:
        with console.status("[bold green]Analisando frota...[/]"):
            resposta = requests.get(f"{sessao.BASE_URL}/veiculos", headers=sessao.get_headers())
            
        veiculos = resposta.json()
        if not veiculos: return

        # Agrupamento
        contagem = {}
        for v in veiculos:
            ano = v["ano"]
            contagem[ano] = contagem.get(ano, 0) + 1
            
        # Ordena pelos anos (Crescente)
        anos_ordenados = sorted(contagem.keys())
        max_valor = max(contagem.values()) # Para normalizar a escala do gráfico

        console.print("\n[bold cyan]Ano   | Gráfico[/]")
        console.print("-" * 40)
        
        for i, ano in enumerate(anos_ordenados):
            qtd = contagem[ano]
            # Normaliza a barra para caber na tela (max 50 chars)
            tamanho_barra = int((qtd / max_valor) * 40)
            cor = CORES[i % len(CORES)]
            barra = "█" * tamanho_barra
            
            console.print(f"{ano}  | [{cor}]{barra}[/] ({qtd})")

    except Exception as e:
        console.print(f"[red]Erro: {e}[/]")
    
    input("\nPressione Enter para continuar...")
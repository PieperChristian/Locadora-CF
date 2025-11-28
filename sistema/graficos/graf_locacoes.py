import requests
from datetime import datetime
from rich.console import Console
from rich.prompt import IntPrompt
from funcoes.gerais import titulo
import funcoes.sessao as sessao

console = Console()

def locacoes_por_mes():
    titulo("Gráfico: Locações por Mês")
    
    # Pergunta o ano para filtrar
    ano_atual = datetime.now().year
    ano_filtro = IntPrompt.ask("Informe o Ano para análise", default=ano_atual)
    
    try:
        with console.status(f"[bold blue]Buscando locações de {ano_filtro}...[/]"):
            resposta = requests.get(f"{sessao.BASE_URL}/alugueis", headers=sessao.get_headers())
            
        if resposta.status_code != 200:
            console.print("[red]Erro na API.[/]")
            return

        alugueis = resposta.json()
        
        # Inicializa contador zerado para os 12 meses
        # {1: 0, 2: 0, ..., 12: 0}
        meses = {i: 0 for i in range(1, 13)}
        
        total_ano = 0
        
        for a in alugueis:
            # Data vem como "2025-11-28T..."
            data_str = a["dataHoraRetirada"]
            # Converte para objeto datetime
            # O replace('Z', '') é para evitar erro em algumas versões do python com timezone
            dt = datetime.fromisoformat(data_str.replace('Z', '+00:00'))
            
            if dt.year == ano_filtro:
                meses[dt.month] += 1
                total_ano += 1

        # Renderização (Estilo Vertical Simplificado)
        console.print(f"\n[bold]Volume de Locações em {ano_filtro}:[/]\n")
        
        max_loc = max(meses.values()) if total_ano > 0 else 1
        nomes_meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", 
                       "Jul", "Ago", "Set", "Out", "Nov", "Dez"]

        for i in range(1, 13):
            qtd = meses[i]
            # Barra proporcional
            tamanho = int((qtd / max_loc) * 50)
            barra = "█" * tamanho
            
            cor = "green" if qtd > 0 else "dim white"
            nome_mes = nomes_meses[i-1]
            
            console.print(f"{nome_mes} | [{cor}]{barra}[/] {qtd}")

        console.print(f"\n[italic]Total acumulado no ano: {total_ano}[/]")

    except Exception as e:
        console.print(f"[red]Erro ao processar dados: {e}[/]")
    
    input("\nPressione Enter para continuar...")
import sys
import os 
from rich.console import Console
from rich.panel import Panel
from funcoes.gerais import titulo
from autenticacao import realizar_login 
import funcoes.sessao as sessao         

# === IMPORTS DOS MÓDULOS ===
from cadastros.clientes import incluir_cliente, alterar_cliente, excluir_cliente, listar_clientes
from cadastros.veiculos import incluir_veiculo, alterar_veiculo, excluir_veiculo, listar_veiculos
from locacoes.alugueis import realizar_aluguel, realizar_devolucao, listar_alugueis
from pesquisas.pesquisas import pesquisar_veiculos_avancada
from pesquisas.pesquisas import pesquisar_veiculos_avancada, pesquisar_locacoes_periodo 
from utilitarios.admin import trocar_senha, fazer_backup, fazer_backup_csv
from graficos.graf_veiculos import veiculos_por_status, veiculos_por_ano
from graficos.graf_locacoes import locacoes_por_mes

console = Console()

if __name__ == "__main__":
    # 1. Autenticação
    if not realizar_login():
        os._exit(0)

    # 2. Loop Principal
    while True:
        titulo(f"Menu Principal - Usuário: {sessao.usuario_nome}")
        
        console.print(Panel.fit(
            "[1] Gestão de Clientes\n"
            "[2] Gestão de Veículos\n"
            "[3] Gestão de Locações (Aluguéis)\n"
            "[4] Gráficos e Relatórios\n"
            "[5] Utilitários do Sistema\n"
            "[0] Finalizar",
            title="Selecione uma Opção",
            border_style="bold blue"
        ))
        
        opcao = console.input("[bold cyan]Opção: [/]").strip()

        # === 1. CLIENTES ===
        if opcao == "1":
            titulo("Gestão de Clientes")
            console.print("[1] Incluir Novo Cliente")
            console.print("[2] Alterar Dados")
            console.print("[3] Excluir Cliente")
            console.print("[4] Listar Clientes")
            console.print("[5] Retornar ao Menu")
            
            sub_opcao = console.input("[bold cyan]Opção: [/]").strip()
            
            if sub_opcao == "1": incluir_cliente()
            elif sub_opcao == "2": alterar_cliente()
            elif sub_opcao == "3": excluir_cliente()
            elif sub_opcao == "4": listar_clientes()
                
        # === 2. VEÍCULOS ===
        elif opcao == "2":
            titulo("Gestão de Veículos")
            console.print("[1] Incluir Novo Veículo")
            console.print("[2] Alterar Veículo")
            console.print("[3] Excluir Veículo")
            console.print("[4] Listar Veículos (Geral)")
            console.print("[5] Pesquisa Avançada (Filtros)")
            console.print("[6] Retornar ao Menu")

            sub_opcao = console.input("[bold cyan]Opção: [/]").strip()

            if sub_opcao == "1": incluir_veiculo()
            elif sub_opcao == "2": alterar_veiculo()
            elif sub_opcao == "3": excluir_veiculo()
            elif sub_opcao == "4": listar_veiculos()
            elif sub_opcao == "5": pesquisar_veiculos_avancada()
            
        # === 3. LOCAÇÕES ===
        elif opcao == "3":
            titulo("Gestão de Locações")
            console.print("[1] Realizar Aluguel (Retirada)")
            console.print("[2] Registrar Devolução")
            console.print("[3] Listar Locações (Geral)")
            console.print("[4] Pesquisar por Período")
            console.print("[5] Retornar ao Menu")
            
            sub_opcao = console.input("[bold cyan]Opção: [/]").strip()
            
            if sub_opcao == "1": realizar_aluguel()
            elif sub_opcao == "2": realizar_devolucao()
            elif sub_opcao == "3": listar_alugueis()
            elif sub_opcao == "4": pesquisar_locacoes_periodo()

        # === 4. GRÁFICOS (Futuro) ===
        elif opcao == "4":
            titulo("Gráficos Gerenciais")
            console.print("[1] Frota por Status (Pizza/Barras)")
            console.print("[2] Frota por Ano (Cronologia)")
            console.print("[3] Locações por Mês (Evolução)")
            console.print("[4] Retornar")

            sub_opcao = console.input("[bold cyan]Opção: [/]").strip()

            if sub_opcao == "1": veiculos_por_status()
            elif sub_opcao == "2": veiculos_por_ano()
            elif sub_opcao == "3": locacoes_por_mes()

        # === 5. UTILITÁRIOS (Futuro) ===
        elif opcao == "5":
            titulo("Utilitários do Sistema")
            console.print("[1] Fazer Backup Completo (JSON)")
            console.print("[2] Exportar Dados para Excel (CSV)")
            console.print("[3] Alterar Minha Senha")
            console.print("[4] Retornar ao Menu")

            sub_opcao = console.input("[bold cyan]Opção: [/]").strip()

            if sub_opcao == "1": fazer_backup()
            elif sub_opcao == "2": fazer_backup_csv()
            elif sub_opcao == "3": trocar_senha()

        # === 0. SAIR ===
        elif opcao == "0":
            console.print("\n[green]Sistema finalizado com sucesso. Até logo![/]")
            os._exit(0)
        
        else:
            console.print("[red]Opção inválida![/]")
            input("Pressione Enter para tentar novamente...")
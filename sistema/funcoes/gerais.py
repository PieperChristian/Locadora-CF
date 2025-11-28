import os
from rich.console import Console

console = Console()

def titulo(texto):
    # Limpa a tela (funciona em Windows, Mac e Linux)
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Exibe o cabeçalho estilizado
    console.rule("[bold blue]LOCADORA DE VEÍCULOS CF")    
    console.rule(f"[bold cyan]{texto}")
    console.rule()
    print()
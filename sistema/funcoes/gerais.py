import os
from rich.console import Console

console = Console()

def titulo(texto):
    os.system('cls' if os.name == 'nt' else 'clear')
    
    console.rule("[bold blue]LOCADORA DE VEÍCULOS CF")    
    console.rule(f"[bold cyan]{texto}")
    console.rule()
    print()
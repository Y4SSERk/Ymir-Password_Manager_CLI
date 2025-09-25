from rich.console import Console
from rich.prompt import Prompt

console = Console()


def prompt_master_password() -> str:
    """Secure password prompt with confirmation"""
    while True:
        password: str = Prompt.ask(
            "[bold red]🔒 Enter master password[/bold red]", password=True
        )
        confirm: str = Prompt.ask(
            "[bold red]🔒 Confirm master password[/bold red]", password=True
        )

        if password == confirm:
            return password
        else:
            console.print("[red]❌ Passwords don't match. Try again.[/red]")

from rich.console import Console
from rich.panel import Panel
from rich.prompt import IntPrompt
from rich.table import Table

console = Console()


def show_main_menu() -> None:

    menu_options = {
        1: ("Add Password", "Add a new password entry"),
        2: ("Search Passwords", "Find existing passwords"),
        3: ("List All", "View all password entries"),
        4: ("Generate Password", "Create a strong random password"),
        5: ("Export Vault", "Backup your password vault"),
        6: ("Exit", "Close the application"),
    }

    while True:
        console.clear()
        console.print(
            Panel.fit(
                "[bold cyan]🔐 Ymir Password Manager[/bold cyan]",
                subtitle="[italic]Secure. Simple. Professional.[/italic]",
            )
        )

        # Create menu table
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Option", style="cyan", width=8)
        table.add_column("Action", style="white", width=20)
        table.add_column("Description", style="dim")

        for num, (action, desc) in menu_options.items():
            table.add_row(str(num), action, desc)

        console.print(table)
        console.print()

        choice = IntPrompt.ask(
            "[bold green]Choose an option[/bold green]",
            choices=[str(i) for i in menu_options.keys()],
            show_choices=False,
        )

        if choice == 1:

            pass
        elif choice == 6:
            console.print("[green]👋 Goodbye![/green]")
            break

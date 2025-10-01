from typing import Any

from ..commands import CommandDispatcher


def show_main_menu(auth_manager: Any) -> None:
    """Beautiful main menu with Rich"""
    from rich import box
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import IntPrompt
    from rich.table import Table

    console = Console()
    dispatcher = CommandDispatcher(auth_manager)

    menu_options = {
        1: ("+ Add Password", "Add a new password entry"),
        2: ("🔍 Search Passwords", "Find existing passwords"),
        3: ("📋 List All", "View all password entries"),
        4: ("✏️  Edit Entry", "Modify an existing entry"),
        5: ("🔄 Generate Password", "Create a strong random password"),
        6: ("❌ Exit", "Close the application"),
    }

    while True:
        console.clear()
        console.print(
            Panel.fit(
                "[bold cyan]🔐 Ymir Password Manager[/bold cyan]",
                subtitle="[italic]Secure. Simple. Professional.[/italic]",
                border_style="cyan",
            )
        )

        # Create menu table
        table = Table(show_header=False, box=box.ROUNDED, style="white")
        table.add_column("Option", style="cyan", width=8)
        table.add_column("Action", style="white", width=20)
        table.add_column("Description", style="dim")

        for num, (action, desc) in menu_options.items():
            table.add_row(f"[{num}]", action, desc)

        console.print(table)
        console.print()

        choice = IntPrompt.ask(
            "[bold green]Choose an option[/bold green]",
            choices=[str(i) for i in menu_options.keys()],
            show_choices=False,
        )

        if choice == 1:
            dispatcher.execute(["add"])
        elif choice == 2:
            dispatcher.execute(["search"])
        elif choice == 3:
            dispatcher.execute(["list"])
        elif choice == 4:
            dispatcher.execute(["edit"])
        elif choice == 5:
            dispatcher.execute(["generate"])
        elif choice == 6:
            console.print("[green]👋 Goodbye![/green]")
            break

        if choice != 6:
            console.print("\n[dim]Press Enter to continue...[/dim]")
            input()

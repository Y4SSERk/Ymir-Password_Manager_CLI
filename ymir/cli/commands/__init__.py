from typing import Any, Dict, List, Type

from rich.console import Console

console = Console()


class CommandDispatcher:
    def __init__(self) -> None:
        self.commands: Dict[str, Type[Any]] = {}
        self._load_commands()

    def _load_commands(self) -> None:
        """Dynamically load available commands"""
        self.commands = {}

    def execute(self, args: List[str]) -> None:
        if not args or args[0] in ("-h", "--help"):
            self.show_help()
            return

        command_name = args[0]
        console.print(f"[yellow]🛠️  Command '{command_name}' coming soon![/yellow]")
        console.print(
            "[cyan]📋 Available now: interactive menu (run 'ymir' without arguments)[/cyan]"
        )

    def show_help(self) -> None:
        """Show beautiful command help"""
        from rich.panel import Panel
        from rich.table import Table

        console.print(
            Panel.fit(
                "[bold cyan]🔐 Ymir Password Manager - Command Reference[/bold cyan]"
            )
        )

        table = Table(show_header=True, header_style="bold green")
        table.add_column("Command", style="cyan", width=12)
        table.add_column("Description", style="white")
        table.add_column("Status", style="yellow")

        commands_info = [
            ("add", "Add new password entry", "Coming soon"),
            ("search", "Search passwords", "Coming soon"),
            ("list", "List all entries", "Coming soon"),
            ("generate", "Generate password", "Coming soon"),
            ("export", "Export vault", "Coming soon"),
        ]

        for cmd, desc, status in commands_info:
            table.add_row(cmd, desc, status)

        console.print(table)
        console.print(
            "\n[green]✅ Available now: Run 'ymir' for interactive menu[/green]"
        )

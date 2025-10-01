from typing import Any, Dict, List, Type

from .add import AddCommand
from .base import BaseCommand
from .edit import EditCommand  # Add this import
from .generate import GenerateCommand
from .list import ListCommand
from .search import SearchCommand


class CommandDispatcher:
    def __init__(self, auth_manager: Any) -> None:
        self.auth_manager = auth_manager
        self.commands: Dict[str, Type[BaseCommand]] = {
            "add": AddCommand,
            "search": SearchCommand,
            "list": ListCommand,
            "generate": GenerateCommand,
            "edit": EditCommand,  # Add edit command
        }

    def execute(self, args: List[str]) -> None:
        from rich.console import Console

        console = Console()

        if not args or args[0] in ("-h", "--help"):
            self.show_help()
            return

        command_name = args[0]
        if command_name in self.commands:
            try:
                command = self.commands[command_name](self.auth_manager)
                command.execute(args[1:])
            except Exception as e:
                console.print(f"[red]❌ Error: {e}[/red]")
        else:
            console.print(f"[red]❌ Unknown command: {command_name}[/red]")
            self.show_help()

    def show_help(self) -> None:
        from rich.console import Console
        from rich.panel import Panel
        from rich.table import Table

        console = Console()

        console.print(
            Panel.fit(
                "[bold cyan]🔐 Ymir Password Manager - Command Reference[/bold cyan]",
                border_style="cyan",
            )
        )

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Command", style="cyan", width=12)
        table.add_column("Description", style="white")
        table.add_column("Usage", style="dim")

        for cmd_name, cmd_class in self.commands.items():
            cmd = cmd_class(self.auth_manager)
            usage_examples = {
                "add": "ymir add <service> <username> <password> [tags...]",
                "search": "ymir search <query>",
                "list": "ymir list",
                "generate": "ymir generate [length]",
                "edit": "ymir edit",  # Add edit usage
            }
            table.add_row(cmd.name, cmd.description, usage_examples.get(cmd_name, ""))

        console.print(table)
        console.print(
            "\n[green]💡 Run 'ymir' without arguments for interactive menu[/green]"
        )

from typing import List

from ymir.core.models.password_entry import PasswordEntry

from .base import BaseCommand


class ListCommand(BaseCommand):
    @property
    def name(self) -> str:
        return "list"

    @property
    def description(self) -> str:
        return "List all password entries"

    def execute(self, args: List[str]) -> None:
        from rich.console import Console

        console = Console()

        try:
            manager = self.auth_manager.get_manager()
            entries = manager.get_all_entries()

            self._display_entries(entries)

        except Exception as e:
            console.print(f"[red]❌ Error listing entries: {e}[/red]")

    def _display_entries(self, entries: List[PasswordEntry]) -> None:
        """Display all entries in a beautiful table"""
        from rich.console import Console
        from rich.table import Table

        console = Console()

        if not entries:
            console.print("[yellow]📭 No password entries found[/yellow]")
            return

        table = Table(
            title="🔐 All Password Entries",
            show_header=True,
            header_style="bold green",
            title_style="bold white",
        )
        table.add_column("#", style="dim", width=4, justify="right")
        table.add_column("Service", style="cyan", min_width=20)
        table.add_column("Username", style="green", min_width=15)
        table.add_column("Tags", style="yellow", min_width=15)

        for i, entry in enumerate(entries, 1):
            tags_display = (
                ", ".join(entry.tags) if hasattr(entry, "tags") and entry.tags else ""
            )
            table.add_row(str(i), entry.service, entry.username, tags_display)

        console.print(table)
        console.print(f"[dim]Total: {len(entries)} entries[/dim]")

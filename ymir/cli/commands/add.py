from typing import List

import pyperclip
from rich.console import Console
from rich.prompt import Confirm, Prompt

from ymir.core.models.password_entry import PasswordEntry

from .base import BaseCommand

console = Console()


class AddCommand(BaseCommand):
    @property
    def name(self) -> str:
        return "add"

    @property
    def description(self) -> str:
        return "Add a new password entry"

    def execute(self, args: List[str]) -> None:
        if len(args) >= 3:
            # Direct arguments: ymir add service username password
            service, username, password = args[0], args[1], args[2]
            tags = args[3:] if len(args) > 3 else []
            self._add_entry(service, username, password, tags)
        else:
            # Interactive mode
            self._interactive_add()

    def _interactive_add(self) -> None:
        """Interactive add with rich prompts"""
        console.print("[bold cyan]+ Add New Password Entry[/bold cyan]")

        service = Prompt.ask("[green]Service/Website[/green]")
        if not service:
            console.print("[red]❌ Service is required[/red]")
            return

        username = Prompt.ask("[green]Username/Email[/green]")
        if not username:
            console.print("[red]❌ Username is required[/red]")
            return

        password = Prompt.ask("[green]Password[/green]", password=True)
        if not password:
            console.print("[red]❌ Password is required[/red]")
            return

        # Optional tags
        tags_input = Prompt.ask(
            "[dim]Tags (comma-separated, optional)[/dim]", default=""
        )
        tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]

        # Optional note
        note = Prompt.ask("[dim]Note (optional)[/dim]", default="")

        # Confirm
        console.print(f"\n[cyan]Service:[/cyan] {service}")
        console.print(f"[cyan]Username:[/cyan] {username}")
        console.print(f"[cyan]Tags:[/cyan] {', '.join(tags) if tags else 'None'}")
        console.print(f"[cyan]Note:[/cyan] {note if note else 'None'}")

        if Confirm.ask("[yellow]Add this entry?[/yellow]"):
            self._add_entry(service, username, password, tags, note)
        else:
            console.print("[yellow]❌ Entry cancelled[/yellow]")

    def _add_entry(
        self,
        service: str,
        username: str,
        password: str,
        tags: List[str],
        note: str = "",
    ) -> None:
        """Actually add the entry to storage"""
        try:
            manager = self.auth_manager.get_manager()
            entry = PasswordEntry(
                service, username, password, tags=set(tags), note=note
            )
            manager.add_entry(entry)

            # Auto-copy password to clipboard
            try:
                pyperclip.copy(password)
                console.print(
                    "[green]✅ Password entry added successfully! (password copied to clipboard)[/green]"
                )
            except Exception:
                console.print("[green]✅ Password entry added successfully![/green]")
                console.print("[yellow]⚠️  Could not copy to clipboard[/yellow]")

        except Exception as e:
            console.print(f"[red]❌ Error adding entry: {e}[/red]")

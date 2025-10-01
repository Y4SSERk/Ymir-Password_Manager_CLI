from typing import Any, List, Optional

from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.table import Table

from ymir.core.models.password_entry import PasswordEntry

from .base import BaseCommand

console = Console()


class EditCommand(BaseCommand):
    @property
    def name(self) -> str:
        return "edit"

    @property
    def description(self) -> str:
        return "Edit an existing password entry"

    def execute(self, args: List[str]) -> None:
        try:
            manager = self.auth_manager.get_manager()
            entries = manager.get_all_entries()

            if not entries:
                console.print("[yellow]📭 No password entries found to edit[/yellow]")
                return

            # Show entries for selection
            self._display_entries_for_selection(entries)

            # Let user select entry to edit
            entry_index = self._select_entry(entries)
            if entry_index is None:
                return

            entry_to_edit = entries[entry_index]
            self._edit_entry_interactive(entry_to_edit, manager)

        except Exception as e:
            console.print(f"[red]❌ Error editing entry: {e}[/red]")

    def _display_entries_for_selection(self, entries: List[PasswordEntry]) -> None:
        """Display entries in a table for selection"""
        table = Table(
            title="Select Entry to Edit", show_header=True, header_style="bold blue"
        )
        table.add_column("#", style="dim", width=4, justify="right")
        table.add_column("Service", style="cyan", min_width=20)
        table.add_column("Username", style="green", min_width=15)
        table.add_column("Tags", style="yellow", min_width=15)
        table.add_column("Note", style="dim", min_width=20)

        for i, entry in enumerate(entries, 1):
            tags_display = ", ".join(entry.tags) if entry.tags else ""
            note_display = entry.note if entry.note else ""
            table.add_row(
                str(i), entry.service, entry.username, tags_display, note_display
            )

        console.print(table)

    def _select_entry(self, entries: List[PasswordEntry]) -> Optional[int]:
        """Let user select an entry to edit"""
        from rich.prompt import IntPrompt

        try:
            choice = IntPrompt.ask(
                "[green]Select entry number to edit[/green]",
                choices=[str(i) for i in range(1, len(entries) + 1)],
                show_choices=False,
            )
            return int(choice) - 1
        except Exception:
            return None

    def _edit_entry_interactive(self, entry: PasswordEntry, manager: Any) -> None:
        """Interactive editing of an entry"""
        console.print(
            f"[bold cyan]✏️  Editing: {entry.service} - {entry.username}[/bold cyan]"
        )

        # Show current values
        console.print("\n[dim]Current values:[/dim]")
        console.print(f"  Service: {entry.service}")
        console.print(f"  Username: {entry.username}")
        console.print(f"  Tags: {', '.join(entry.tags) if entry.tags else 'None'}")
        console.print(f"  Note: {entry.note if entry.note else 'None'}")
        console.print()

        # Edit fields
        new_service = Prompt.ask("[green]New service[/green]", default=entry.service)
        new_username = Prompt.ask("[green]New username[/green]", default=entry.username)

        # Password - optional to change
        change_password = Confirm.ask(
            "[yellow]Change password?[/yellow]", default=False
        )
        if change_password:
            new_password = Prompt.ask("[green]New password[/green]", password=True)
        else:
            new_password = entry.password

        # Tags
        current_tags = ", ".join(entry.tags) if entry.tags else ""
        new_tags_input = Prompt.ask(
            "[green]New tags (comma-separated)[/green]", default=current_tags
        )
        new_tags = [tag.strip() for tag in new_tags_input.split(",") if tag.strip()]

        # Note
        new_note = Prompt.ask("[green]New note[/green]", default=entry.note or "")

        # Confirm changes
        console.print("\n[cyan]New values:[/cyan]")
        console.print(f"  Service: {new_service}")
        console.print(f"  Username: {new_username}")
        console.print(
            f"  Password: {'[CHANGED]' if change_password else '[UNCHANGED]'}"
        )
        console.print(f"  Tags: {', '.join(new_tags) if new_tags else 'None'}")
        console.print(f"  Note: {new_note if new_note else 'None'}")

        if Confirm.ask("[yellow]Apply these changes?[/yellow]"):
            # Update entry
            entry.service = new_service
            entry.username = new_username
            entry.password = new_password
            entry.tags = set(new_tags)
            entry.note = new_note
            entry.updated_at = __import__("datetime").datetime.now()

            # Save changes
            manager._save()
            console.print("[green]✅ Entry updated successfully![/green]")
        else:
            console.print("[yellow]❌ Edit cancelled[/yellow]")

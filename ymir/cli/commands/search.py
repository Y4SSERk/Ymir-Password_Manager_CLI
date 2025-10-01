from typing import List

from ymir.core.models.password_entry import PasswordEntry
from ymir.core.models.search_query import SearchQuery

from .base import BaseCommand


class SearchCommand(BaseCommand):
    @property
    def name(self) -> str:
        return "search"

    @property
    def description(self) -> str:
        return "Search password entries"

    def execute(self, args: List[str]) -> None:
        from rich.console import Console
        from rich.prompt import Prompt

        console = Console()

        if args:
            # Direct search: ymir search query
            query_text = " ".join(args)
            self._perform_search(query_text)
        else:
            # Interactive search
            query_text = Prompt.ask("[green]Search term[/green]")
            if query_text:
                self._perform_search(query_text)
            else:
                console.print("[yellow]⚠️  No search term provided[/yellow]")

    def _perform_search(self, query_text: str) -> None:
        """Perform the search and display results"""
        from rich.console import Console

        console = Console()

        try:
            manager = self.auth_manager.get_manager()
            query = SearchQuery(search_text=query_text)
            results = manager.search_entries(query)

            self._display_results(results, query_text)

        except Exception as e:
            console.print(f"[red]❌ Error searching: {e}[/red]")

    def _display_results(self, results: List[PasswordEntry], query: str) -> None:
        """Display search results in a beautiful table"""
        from rich.console import Console
        from rich.table import Table

        console = Console()

        if not results:
            console.print(f"[yellow]🔍 No results found for '{query}'[/yellow]")
            return

        table = Table(
            title=f"🔍 Search Results for '{query}'",
            show_header=True,
            header_style="bold blue",
            title_style="bold white",
        )
        table.add_column("Service", style="cyan", min_width=20)
        table.add_column("Username", style="green", min_width=15)
        table.add_column("Tags", style="yellow", min_width=15)

        for entry in results:
            tags_display = (
                ", ".join(entry.tags) if hasattr(entry, "tags") and entry.tags else ""
            )
            table.add_row(entry.service, entry.username, tags_display)

        console.print(table)
        console.print(f"[dim]Found {len(results)} result(s)[/dim]")

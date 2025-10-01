import secrets
import string
from typing import List

from .base import BaseCommand


class GenerateCommand(BaseCommand):
    @property
    def name(self) -> str:
        return "generate"

    @property
    def description(self) -> str:
        return "Generate a strong random password"

    def execute(self, args: List[str]) -> None:
        if args and args[0].isdigit():
            # Direct generation: ymir generate 16
            length = int(args[0])
            password = self._generate_password(length)
            self._handle_generated_password(password)
        else:
            # Interactive generation
            self._interactive_generate()

    def _interactive_generate(self) -> None:
        """Interactive password generation"""
        from rich.console import Console
        from rich.prompt import Confirm, IntPrompt

        console = Console()

        console.print("[bold cyan]🔄 Generate Strong Password[/bold cyan]")

        length = IntPrompt.ask(
            "[green]Password length[/green]", default=16, show_default=True
        )

        if length < 8:
            console.print("[red]❌ Password length must be at least 8[/red]")
            return

        use_uppercase = Confirm.ask(
            "[green]Include uppercase letters?[/green]", default=True
        )
        use_numbers = Confirm.ask("[green]Include numbers?[/green]", default=True)
        use_symbols = Confirm.ask("[green]Include symbols?[/green]", default=True)

        password = self._generate_password(
            length, use_uppercase, use_numbers, use_symbols
        )
        self._handle_generated_password(password)

    def _generate_password(
        self,
        length: int = 16,
        use_uppercase: bool = True,
        use_numbers: bool = True,
        use_symbols: bool = True,
    ) -> str:
        """Generate a strong random password"""
        characters = string.ascii_lowercase

        if use_uppercase:
            characters += string.ascii_uppercase
        if use_numbers:
            characters += string.digits
        if use_symbols:
            characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"

        if not characters:
            characters = string.ascii_letters + string.digits

        return "".join(secrets.choice(characters) for _ in range(length))

    def _handle_generated_password(self, password: str) -> None:
        """Handle the generated password - copy to clipboard without displaying it"""
        import pyperclip
        from rich.console import Console
        from rich.panel import Panel

        console = Console()

        # Auto-copy to clipboard
        try:
            pyperclip.copy(password)
            console.print(
                Panel(
                    "[bold green]✅ Password generated and copied to clipboard![/bold green]",
                    title="🔒 Password Generated",
                    title_align="left",
                    border_style="green",
                )
            )
            console.print(
                "[yellow]💡 The password is now in your clipboard - paste it where needed![/yellow]"
            )
            console.print(
                "[dim]🔒 For security, the password is not displayed on screen.[/dim]"
            )

        except Exception:
            console.print(
                Panel(
                    "[bold red]❌ Password generated but could not copy to clipboard[/bold red]",
                    title="⚠️ Clipboard Error",
                    title_align="left",
                    border_style="red",
                )
            )
            console.print(
                "[yellow]Please install pyperclip or fix clipboard access[/yellow]"
            )

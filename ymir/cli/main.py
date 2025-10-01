#!/usr/bin/env python3
"""
Ymir CLI - Secure Password Manager
Hybrid interface: Direct commands OR interactive menu
"""

import sys

from rich.console import Console

from .auth import AuthManager
from .commands import CommandDispatcher
from .interface.menu import show_main_menu

console = Console()


def main() -> None:
    """Main entry point - handles authentication and mode selection"""
    try:
        # Initialize authentication
        auth_manager = AuthManager()

        # Authenticate user
        if not auth_manager.authenticate():
            console.print("[red]❌ Authentication failed. Exiting.[/red]")
            return

        try:
            # Determine mode based on arguments
            if len(sys.argv) > 1:
                # Direct command mode
                dispatcher = CommandDispatcher(auth_manager)
                dispatcher.execute(sys.argv[1:])
            else:
                # Interactive menu mode - PASS auth_manager as argument
                show_main_menu(auth_manager)

        finally:
            # Always close the manager to clear sensitive data
            auth_manager.close()

    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️  Operation cancelled by user[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Unexpected error: {e}[/red]")


if __name__ == "__main__":
    main()

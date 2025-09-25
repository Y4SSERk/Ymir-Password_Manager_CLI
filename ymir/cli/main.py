import sys

from rich.console import Console

from .commands import CommandDispatcher
from .interface.menu import show_main_menu

console = Console()


def main() -> None:
    if len(sys.argv) > 1:
        # Direct command mode
        dispatcher = CommandDispatcher()
        dispatcher.execute(sys.argv[1:])
    else:
        # Interactive menu mode
        show_main_menu()


if __name__ == "__main__":
    main()

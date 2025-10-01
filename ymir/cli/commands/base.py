from abc import ABC, abstractmethod
from typing import Any, List


class BaseCommand(ABC):
    """Abstract base class for all commands"""

    def __init__(self, auth_manager: Any) -> None:
        self.auth_manager = auth_manager

    @abstractmethod
    def execute(self, args: List[str]) -> Any:
        """Execute the command with given arguments"""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Command name"""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Command description for help"""
        pass

    def show_usage(self) -> None:
        """Show command usage examples"""
        from rich.console import Console

        console = Console()
        console.print(f"[yellow]Usage: ymir {self.name} [options][/yellow]")

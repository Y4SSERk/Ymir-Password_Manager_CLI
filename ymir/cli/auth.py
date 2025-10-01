import getpass
from typing import Optional

from rich.console import Console

from ymir.storage.password_manager import PasswordManager
from ymir.utils.config import Config

console = Console()


class AuthManager:
    """Handles user authentication and vault management"""

    def __init__(self) -> None:
        self.config: Config = Config()
        self.manager: Optional[PasswordManager] = None

    def authenticate(self) -> bool:
        """Authenticate user and initialize PasswordManager"""
        console.print("[bold cyan]🔐 Ymir Password Manager[/bold cyan]")

        if not self.config.vault_exists():
            return self._create_new_vault()
        else:
            return self._unlock_existing_vault()

    def _create_new_vault(self) -> bool:
        """Create a new password vault"""
        console.print("[yellow]📁 No existing vault found. Let's create one![/yellow]")

        while True:
            master_password = getpass.getpass("🔒 Create master password: ")
            confirm_password = getpass.getpass("🔒 Confirm master password: ")

            if master_password != confirm_password:
                console.print("[red]❌ Passwords don't match. Try again.[/red]")
                continue

            if len(master_password) < 8:
                console.print("[red]❌ Password must be at least 8 characters.[/red]")
                continue

            try:
                self.config.ensure_config_dir()
                vault_path = self.config.get_vault_path()

                # Create the manager - this will create the vault file
                self.manager = PasswordManager(vault_path, master_password)

                # Add a test entry to ensure vault works
                from ymir.core.models.password_entry import PasswordEntry

                test_entry = PasswordEntry("example.com", "user", "password")
                self.manager.add_entry(test_entry)

                console.print("[green]✅ Vault created successfully![/green]")
                return True

            except Exception as e:
                console.print(f"[red]❌ Failed to create vault: {e}[/red]")
                return False

    def _unlock_existing_vault(self) -> bool:
        """Unlock existing vault with master password"""
        attempts = 3

        while attempts > 0:
            master_password = getpass.getpass("🔒 Enter master password: ")

            try:
                vault_path = self.config.get_vault_path()

                # Try to create the manager with the provided password
                self.manager = PasswordManager(vault_path, master_password)

                # Try to load entries - this will fail if password is wrong
                # due to decryption errors
                self.manager.get_all_entries()

                # If we get here, password is correct
                console.print("[green]✅ Vault unlocked![/green]")
                return True

            except Exception as e:
                # Check if it's a decryption error (wrong password)
                error_msg = str(e).lower()
                if any(
                    keyword in error_msg
                    for keyword in ["decrypt", "password", "key", "integrity", "cipher"]
                ):
                    attempts -= 1
                    if attempts > 0:
                        console.print(
                            f"[red]❌ Invalid password. {attempts} attempts remaining.[/red]"
                        )
                    else:
                        console.print(
                            "[red]❌ Too many failed attempts. Exiting.[/red]"
                        )
                        return False
                else:
                    # It's some other error, not a password issue
                    console.print(f"[red]❌ Error accessing vault: {e}[/red]")
                    return False

        return False

    def get_manager(self) -> PasswordManager:
        """Get the authenticated PasswordManager instance"""
        if self.manager is None:
            raise RuntimeError("Not authenticated")
        return self.manager

    def close(self) -> None:
        """Close the manager and clear sensitive data"""
        if self.manager:
            self.manager.close()

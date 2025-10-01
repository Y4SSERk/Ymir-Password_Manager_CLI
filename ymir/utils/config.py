from pathlib import Path


class Config:
    """Configuration manager for Ymir"""

    def __init__(self) -> None:  # Add return type
        self.config_dir = Path.home() / ".ymir"
        self.vault_path = self.config_dir / "vault.ymir"
        self.config_file = self.config_dir / "config.json"

    def ensure_config_dir(self) -> None:  # Add return type
        """Ensure configuration directory exists"""
        self.config_dir.mkdir(exist_ok=True, mode=0o700)

    def get_vault_path(self) -> Path:
        """Get vault file path"""
        self.ensure_config_dir()
        return self.vault_path

    def vault_exists(self) -> bool:
        """Check if vault file exists"""
        return self.vault_path.exists()

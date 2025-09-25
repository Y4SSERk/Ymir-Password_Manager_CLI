import json
import stat
import tempfile
from pathlib import Path
from typing import List

from ymir.core.models.password_entry import PasswordEntry
from ymir.security.encryption import EncryptionService, SecurityError


class JsonStorage:

    def __init__(self, storage_path: Path, encryption_service: EncryptionService):
        self.storage_path = storage_path
        self.encryption_service = encryption_service
        self._ensure_secure_directory()

    def _ensure_secure_directory(self) -> None:
        storage_dir = self.storage_path.parent
        storage_dir.mkdir(parents=True, exist_ok=True)
        storage_dir.chmod(stat.S_IRWXU)  # 700 permissions

    def save_entries(self, entries: List[PasswordEntry]) -> None:
        """Save entries to encrypted JSON storage with atomic write."""
        try:
            # Create temporary file in the same directory
            temp_dir = self.storage_path.parent
            temp_dir.mkdir(parents=True, exist_ok=True)

            with tempfile.NamedTemporaryFile(
                mode="w", dir=temp_dir, prefix="tmp", suffix=".vault", delete=False
            ) as tmp_file:
                tmp_path = Path(tmp_file.name)

                # Serialize and encrypt data
                serialized_data = [entry.to_dict() for entry in entries]
                json_data = json.dumps(serialized_data, indent=2)
                encrypted_data = self.encryption_service.encrypt(json_data)

                # Write to temporary file
                tmp_file.write(encrypted_data)

            # Atomic replace on Windows - handle file existence
            if self.storage_path.exists():
                self.storage_path.unlink()  # Remove existing file first

            # Now rename should work
            tmp_path.rename(self.storage_path)

        except Exception as e:
            # Clean up temporary file on error
            if "tmp_path" in locals() and tmp_path.exists():
                tmp_path.unlink()
            raise e

    def load_entries(self) -> List[PasswordEntry]:
        if not self.storage_path.exists():
            return []

        try:
            encrypted_data = self.storage_path.read_text(encoding="utf-8")
            decrypted_data = self.encryption_service.decrypt(encrypted_data)
            data = json.loads(decrypted_data)

            if not isinstance(data, dict) or "entries" not in data:
                raise SecurityError("Invalid storage format")

            entries = []
            for entry_data in data["entries"]:
                try:
                    entries.append(PasswordEntry.from_dict(entry_data))
                except (KeyError, ValueError):
                    continue  # Skip invalid entries

            return entries

        except Exception as e:
            raise SecurityError(f"Failed to load entries: {e!s}") from e

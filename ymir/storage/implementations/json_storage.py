import base64
import json
from pathlib import Path
from typing import List

from ymir.core.models.password_entry import PasswordEntry
from ymir.security.encryption import EncryptionService, SecurityError


class JsonStorage:
    """JSON-based storage with encryption"""

    def __init__(self, storage_path: Path, encryption_service: EncryptionService):
        self.storage_path = storage_path
        self.encryption_service = encryption_service

    def load_entries(self) -> List[PasswordEntry]:
        """Load entries from encrypted JSON storage"""
        if not self.storage_path.exists():
            return []

        try:
            with open(self.storage_path, "r") as f:
                file_content = f.read().strip()

            if not file_content:
                return []

            # Parse the stored data
            data = json.loads(file_content)

            # Extract salt and encrypted data
            salt_b64 = data.get("salt")
            encrypted_data = data.get("data")

            if not salt_b64 or not encrypted_data:
                raise SecurityError("Invalid vault file format")

            # Convert salt from base64 back to bytes
            salt = base64.b64decode(salt_b64)

            # Set the salt in the encryption service to use the same one
            self.encryption_service.set_salt(salt)

            # Decrypt the data
            decrypted_data = self.encryption_service.decrypt(encrypted_data)
            serialized_entries = json.loads(decrypted_data)

            entries = []
            for entry_data in serialized_entries:
                entry = PasswordEntry.from_dict(entry_data)
                entries.append(entry)

            return entries

        except Exception as e:
            raise SecurityError(f"Failed to load entries: {e!s}") from e

    def save_entries(self, entries: List[PasswordEntry]) -> None:
        """Save entries to encrypted JSON storage with atomic write"""
        import tempfile

        try:
            # Create temporary file in the same directory
            temp_dir = self.storage_path.parent
            temp_dir.mkdir(parents=True, exist_ok=True)

            with tempfile.NamedTemporaryFile(
                mode="w", dir=temp_dir, prefix="tmp", suffix=".vault", delete=False
            ) as tmp_file:
                tmp_path = Path(tmp_file.name)

                # Serialize entries
                serialized_data = [entry.to_dict() for entry in entries]
                json_data = json.dumps(serialized_data, indent=2)

                # Encrypt data (using the current salt in encryption_service)
                encrypted_data = self.encryption_service.encrypt(json_data)

                # Get the salt used for encryption
                salt = self.encryption_service.get_salt()
                salt_b64 = base64.b64encode(salt).decode()

                # Store both salt and encrypted data
                storage_data = {"salt": salt_b64, "data": encrypted_data}

                # Write to temporary file
                json.dump(storage_data, tmp_file, indent=2)

            # Atomic replace
            if self.storage_path.exists():
                self.storage_path.unlink()

            tmp_path.rename(self.storage_path)

        except Exception as e:
            # Clean up temporary file on error
            if "tmp_path" in locals() and tmp_path.exists():
                tmp_path.unlink()
            raise e

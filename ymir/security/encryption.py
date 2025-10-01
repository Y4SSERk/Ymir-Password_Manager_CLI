import base64
import hashlib
import hmac
import secrets
from typing import Optional

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from .memory import SecurityError


class EncryptionService:
    def __init__(self, master_password: str, salt: Optional[bytes] = None):
        # Store the salt first
        self._salt = salt or secrets.token_bytes(32)
        # Then derive keys using the salt
        self._master_password = master_password
        self._derive_keys()

    def _derive_keys(self) -> None:
        """Derive encryption keys using the current salt"""
        # Derive main encryption key
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self._salt,
            iterations=600000,
        )
        key = kdf.derive(self._master_password.encode())
        self._key = base64.urlsafe_b64encode(key)
        self._fernet = Fernet(self._key)

        # Derive HMAC key
        hmac_kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self._salt + b"hmac",
            iterations=100000,
        )
        self._hmac_key = hmac_kdf.derive(self._master_password.encode())

    def encrypt(self, data: str) -> str:
        encrypted: bytes = self._fernet.encrypt(data.encode())
        hmac_code: bytes = hmac.new(self._hmac_key, encrypted, hashlib.sha256).digest()
        combined: bytes = hmac_code + encrypted
        return base64.urlsafe_b64encode(combined).decode()

    def decrypt(self, encrypted_data: str) -> str:
        try:
            combined: bytes = base64.urlsafe_b64decode(encrypted_data.encode())

            if len(combined) < (32 + 1):
                raise SecurityError("Invalid encrypted data")

            received_hmac = combined[:32]
            encrypted = combined[32:]

            expected_hmac: bytes = hmac.new(
                self._hmac_key, encrypted, hashlib.sha256
            ).digest()
            if not hmac.compare_digest(received_hmac, expected_hmac):
                raise SecurityError("Data integrity check failed")

            decrypted_data: bytes = self._fernet.decrypt(encrypted)
            result: str = decrypted_data.decode("utf-8")
            return result

        except Exception as e:
            raise SecurityError(f"Decryption failed: {e!s}") from e

    def get_salt(self) -> bytes:
        return self._salt

    def set_salt(self, salt: bytes) -> None:
        """Set the salt and re-derive keys (used when loading existing vault)"""
        self._salt = salt
        self._derive_keys()  # Re-derive keys with the new salt

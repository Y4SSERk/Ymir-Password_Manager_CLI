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
        self._salt: bytes = salt or secrets.token_bytes(32)
        self._key: bytes = self._derive_key(master_password)
        self._fernet: Fernet = Fernet(self._key)
        self._hmac_key: bytes = self._derive_hmac_key(master_password)

    def _derive_key(self, master_password: str) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self._salt,
            iterations=600000,  # OWASP recommended
        )
        key: bytes = kdf.derive(master_password.encode())
        return base64.urlsafe_b64encode(key)

    def _derive_hmac_key(self, master_password: str) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self._salt + b"hmac",
            iterations=100000,
        )
        key: bytes = kdf.derive(master_password.encode())
        return key

    def encrypt(self, data: str) -> str:
        encrypted: bytes = self._fernet.encrypt(data.encode())
        hmac_code: bytes = hmac.new(self._hmac_key, encrypted, hashlib.sha256).digest()
        combined: bytes = hmac_code + encrypted
        result: str = base64.urlsafe_b64encode(combined).decode()
        return result

    def decrypt(self, encrypted_data: str) -> str:
        try:
            combined: bytes = base64.urlsafe_b64decode(encrypted_data.encode())

            if len(combined) < (32 + 1):
                raise SecurityError("Invalid encrypted data")

            received_hmac: bytes = combined[:32]
            encrypted: bytes = combined[32:]

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

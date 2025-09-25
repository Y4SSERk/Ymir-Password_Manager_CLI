import gc
import secrets


class SecureMemory:

    @staticmethod
    def secure_bytes(size: int) -> bytes:
        return secrets.token_bytes(size)

    @staticmethod
    def wipe_buffer(buf: bytearray) -> None:
        if buf:
            for i in range(len(buf)):
                buf[i] = secrets.randbelow(256)
            gc.collect()

    @staticmethod
    def create_secure_data(data: str) -> bytearray:
        return bytearray(data.encode("utf-8"))


class SecurityError(Exception):
    pass

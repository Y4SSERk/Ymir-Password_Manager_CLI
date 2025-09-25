import tempfile
from pathlib import Path

import pytest

from ymir.core.models.password_entry import PasswordEntry
from ymir.core.models.search_query import SearchQuery
from ymir.security.encryption import EncryptionService, SecurityError
from ymir.storage.password_manager import PasswordManager  # Fix this import name


def test_encryption_roundtrip():
    service = EncryptionService("test-password")
    data = "sensitive data"

    encrypted = service.encrypt(data)
    decrypted = service.decrypt(encrypted)

    assert decrypted == data
    assert encrypted != data


def test_tamper_detection():
    service = EncryptionService("test-password")
    encrypted = service.encrypt("data")

    tampered = encrypted[:-10] + "AAA"

    with pytest.raises(SecurityError):
        service.decrypt(tampered)


def test_secure_storage():
    with tempfile.TemporaryDirectory() as temp_dir:
        storage_path = Path(temp_dir) / "test.vault"
        manager = PasswordManager(storage_path, "password")  # Fix class name

        entry = PasswordEntry("service.com", "user", "pass")
        manager.add_entry(entry)

        query = SearchQuery(service="service.com")
        results = manager.search_entries(query)
        assert len(results) == 1
        assert results[0].username == "user"

        manager.add_tag_to_entry(entry.id, "financial")
        results = manager.search_entries(SearchQuery(tags=["financial"]))
        assert len(results) == 1

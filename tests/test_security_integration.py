#!/usr/bin/env python3

import tempfile
from pathlib import Path

from ymir.core.models.password_entry import PasswordEntry
from ymir.core.models.search_query import SearchQuery
from ymir.storage.password_manager import PasswordManager


def test_security_integration():
    print("🔒 Testing security integration...")

    with tempfile.TemporaryDirectory() as temp_dir:
        storage_path = Path(temp_dir) / "test.vault"

        # Create secure manager
        manager = PasswordManager(storage_path, "master123")

        # Add entries
        entry = PasswordEntry("bank.com", "user", "securepass")
        manager.add_entry(entry)

        # Search entries
        query = SearchQuery(service="bank.com")
        results = manager.search_entries(query)
        assert len(results) == 1
        assert results[0].username == "user"
        print("✅ Secure storage and retrieval works")

        # Test tag operations
        manager.add_tag_to_entry(entry.id, "financial")
        results = manager.search_entries(SearchQuery(tags=["financial"]))
        assert len(results) == 1
        print("✅ Tag operations work with secure storage")

    print("🎉 Security integration tests passed!")


if __name__ == "__main__":
    test_security_integration()

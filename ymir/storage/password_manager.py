import gc
from pathlib import Path
from typing import List, Optional

from ymir.core.models.password_entry import PasswordEntry
from ymir.core.models.search_query import SearchQuery
from ymir.core.services.search_service import SearchService
from ymir.core.services.tag_service import TagService
from ymir.security.encryption import EncryptionService, SecurityError
from ymir.storage.implementations.json_storage import JsonStorage


class PasswordManager:

    def __init__(self, storage_path: Path, master_password: str):
        self.storage_path = storage_path

        # Initialize services
        self.encryption_service = EncryptionService(master_password)
        self.storage = JsonStorage(storage_path, self.encryption_service)
        self.tag_service = TagService()
        self._entries = self.storage.load_entries()

        # Clear password from memory immediately after use
        master_password = "0" * len(master_password)
        gc.collect()

    def add_entry(self, entry: PasswordEntry) -> None:
        self._entries.append(entry)
        self._save()

    def search_entries(self, query: SearchQuery) -> List[PasswordEntry]:
        search_service = SearchService(self._entries)
        return search_service.search(query)

    def get_all_entries(self) -> List[PasswordEntry]:
        return self._entries.copy()

    def _save(self) -> None:
        try:
            self.storage.save_entries(self._entries)
        except Exception as e:
            self._clear_memory()
            raise SecurityError(f"Save failed: {e!s}") from e

    def add_tag_to_entry(self, entry_id: str, tag: str) -> bool:
        entry = self.get_entry_by_id(entry_id)
        if entry:
            success = self.tag_service.add_tag(entry, tag)
            if success:
                self._save()
            return success
        return False

    def get_entry_by_id(self, entry_id: str) -> Optional[PasswordEntry]:
        for entry in self._entries:
            if entry.id == entry_id:
                return entry
        return None

    def _clear_memory(self) -> None:
        for entry in self._entries:
            if hasattr(entry, "password"):
                entry.password = "0" * len(entry.password)
        self._entries.clear()
        gc.collect()

    def close(self) -> None:
        self._clear_memory()

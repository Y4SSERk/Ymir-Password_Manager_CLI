import re
from typing import Any, List, Optional

from ymir.core.models.password_entry import PasswordEntry
from ymir.core.models.search_query import SearchQuery
from ymir.core.services.tag_service import TagService


class SearchService:
    def __init__(self, entries: List[PasswordEntry]):
        self.entries = entries

    def search(self, query: SearchQuery) -> List[PasswordEntry]:
        if query.is_empty():
            return self._sort_entries(self.entries, query)

        return self._sort_entries(
            [entry for entry in self.entries if self._matches_query(query, entry)],
            query,
        )

    def _matches_query(self, query: SearchQuery, entry: PasswordEntry) -> bool:
        return (
            self._matches_field_search(query, entry)
            and self._matches_text_search(query, entry)
            and self._matches_tag_search(query, entry)
        )

    def _matches_field_search(self, query: SearchQuery, entry: PasswordEntry) -> bool:
        return all(
            [
                self._matches_field(query.service, entry.service),
                self._matches_field(query.username, entry.username),
                self._matches_field(query.note, entry.note),
            ]
        )

    def _matches_field(
        self, search_value: Optional[str], entry_value: Optional[str]
    ) -> bool:
        if not search_value:
            return True
        if not entry_value:
            return False
        return self._text_matches(search_value, entry_value, False)

    def _matches_text_search(self, query: SearchQuery, entry: PasswordEntry) -> bool:
        if not query.search_text:
            return True

        search_text = " ".join(
            [entry.service or "", entry.username or "", entry.note or ""]
        )
        return self._text_matches(query.search_text, search_text, query.case_sensitive)

    def _matches_tag_search(self, query: SearchQuery, entry: PasswordEntry) -> bool:
        if not query.tags:
            return True
        return TagService.matches_tags(entry, query.tags, query.match_all_tags)

    def _text_matches(
        self, search_text: str, target_text: str, case_sensitive: bool
    ) -> bool:
        if not search_text or not target_text:
            return False

        if not case_sensitive:
            search_text = search_text.lower()
            target_text = target_text.lower()

        if "*" in search_text or "?" in search_text:
            return self._wildcard_match(search_text, target_text)

        return search_text in target_text

    def _wildcard_match(self, pattern: str, text: str) -> bool:
        regex_pattern = "".join(
            ".*" if char == "*" else "." if char == "?" else re.escape(char)
            for char in pattern
        )

        try:
            return bool(re.match(f"^{regex_pattern}$", text))
        except re.error:
            return pattern.replace("*", "").replace("?", "") in text

    def _sort_entries(
        self, entries: List[PasswordEntry], query: SearchQuery
    ) -> List[PasswordEntry]:
        if not entries:
            return entries

        reverse = query.sort_descending
        key = {
            "username": lambda x: x.username or "",
            "created_at": lambda x: x.created_at,
            "updated_at": lambda x: x.updated_at,
        }.get(query.sort_by, lambda x: x.service)

        sorted_entries = sorted(entries, key=key, reverse=reverse)
        return sorted_entries[: query.limit] if query.limit else sorted_entries


def search_entries(
    entries: List[PasswordEntry], query: SearchQuery
) -> List[PasswordEntry]:
    return SearchService(entries).search(query)


def search_by_text(
    entries: List[PasswordEntry], search_text: str, **kwargs: Any
) -> List[PasswordEntry]:
    query = SearchQuery(search_text=search_text, **kwargs)
    return search_entries(entries, query)


def search_by_service(
    entries: List[PasswordEntry], service: str, **kwargs: Any
) -> List[PasswordEntry]:
    query = SearchQuery(service=service, **kwargs)
    return search_entries(entries, query)


def search_by_tags(
    entries: List[PasswordEntry],
    tags: List[str],
    match_all: bool = False,
    **kwargs: Any,
) -> List[PasswordEntry]:
    query = SearchQuery(tags=tags, match_all_tags=match_all, **kwargs)
    return search_entries(entries, query)

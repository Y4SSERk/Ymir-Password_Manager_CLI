from typing import List

from ymir.core.models.password_entry import PasswordEntry


class TagService:

    @staticmethod
    def add_tag(entry: PasswordEntry, tag: str) -> bool:
        if not isinstance(tag, str) or not tag.strip():
            return False

        cleaned_tag = tag.strip().lower()
        if cleaned_tag not in entry.tags:
            entry.tags.add(cleaned_tag)
            entry.update_timestamp()
            return True
        return False

    @staticmethod
    def remove_tag(entry: PasswordEntry, tag: str) -> bool:
        if not isinstance(tag, str):
            return False

        cleaned_tag = tag.strip().lower()
        if cleaned_tag in entry.tags:
            entry.tags.remove(cleaned_tag)
            entry.update_timestamp()
            return True
        return False

    @staticmethod
    def has_tag(entry: PasswordEntry, tag: str) -> bool:
        if not isinstance(tag, str):
            return False
        return tag.strip().lower() in entry.tags

    @staticmethod
    def has_any_tag(entry: PasswordEntry, tags: List[str]) -> bool:
        if not tags:
            return False

        search_tags = {tag.strip().lower() for tag in tags if isinstance(tag, str)}
        return bool(entry.tags & search_tags)

    @staticmethod
    def has_all_tags(entry: PasswordEntry, tags: List[str]) -> bool:
        if not tags:
            return False

        search_tags = {tag.strip().lower() for tag in tags if isinstance(tag, str)}
        return search_tags.issubset(entry.tags)

    # Search helper methods
    @staticmethod
    def matches_tags(
        entry: PasswordEntry, search_tags: List[str], match_all: bool = False
    ) -> bool:
        if not search_tags:
            return True

        if match_all:
            return TagService.has_all_tags(entry, search_tags)
        else:
            return TagService.has_any_tag(entry, search_tags)

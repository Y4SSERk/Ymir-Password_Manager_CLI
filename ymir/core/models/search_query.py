from dataclasses import dataclass
from typing import Any, List, Literal, Optional


@dataclass(frozen=True)
class SearchQuery:

    # Field-specific searches
    service: Optional[str] = None
    username: Optional[str] = None
    note: Optional[str] = None
    tags: Optional[List[str]] = None

    # Cross-field text search
    search_text: Optional[str] = None

    # Search options
    case_sensitive: bool = False
    match_all_tags: bool = False

    # Results options
    limit: Optional[int] = None
    sort_by: Literal["service", "username", "created_at", "updated_at"] = "service"
    sort_descending: bool = False

    def __post_init__(self) -> None:
        self._validate_fields()

    def _validate_fields(self) -> None:
        for field in ["service", "username", "note", "search_text"]:
            value = getattr(self, field)
            if value is not None and not isinstance(value, str):
                raise ValueError(f"Field '{field}' must be a string or None")

        if self.tags is not None and not isinstance(self.tags, list):
            raise ValueError("Field 'tags' must be a list or None")

    def is_empty(self) -> bool:
        return all(
            value is None
            or value == ""
            or (isinstance(value, list) and len(value) == 0)
            for value in [
                self.service,
                self.username,
                self.note,
                self.tags,
                self.search_text,
            ]
        )

    def __str__(self) -> str:
        if self.is_empty():
            return "SearchQuery(show all entries)"

        parts = []
        for field in ["service", "username", "note", "search_text"]:
            value = getattr(self, field)
            if value:
                parts.append(f"{field}={value!r}")

        if self.tags:
            parts.append(f"tags={self.tags}")

        return f"SearchQuery({', '.join(parts)})"

    @classmethod
    def create_text_search(cls, search_text: str, **kwargs: Any) -> "SearchQuery":
        return cls(search_text=search_text, **kwargs)

    @classmethod
    def create_service_search(cls, service: str, **kwargs: Any) -> "SearchQuery":
        return cls(service=service, **kwargs)

    @classmethod
    def create_tag_search(
        cls, tags: List[str], match_all: bool = False, **kwargs: Any
    ) -> "SearchQuery":
        return cls(tags=tags, match_all_tags=match_all, **kwargs)

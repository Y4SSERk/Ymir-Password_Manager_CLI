import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class PasswordEntry:

    service: str
    username: str
    password: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    note: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        if not self.service.strip():
            raise ValueError("Service cannot be empty")
        if not self.username.strip():
            raise ValueError("Username cannot be empty")
        if not self.password:
            raise ValueError("Password cannot be empty")
        if self.updated_at < self.created_at:
            self.updated_at = self.created_at

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "service": self.service,
            "username": self.username,
            "password": self.password,
            "note": self.note,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PasswordEntry":
        # Parse timestamps
        created_at = cls._parse_timestamp(data.get("created_at"))
        updated_at = cls._parse_timestamp(data.get("updated_at"), default=created_at)

        if updated_at < created_at:
            updated_at = created_at

        return cls(
            id=data.get("id", str(uuid.uuid4())),
            service=data["service"],
            username=data["username"],
            password=data["password"],
            note=data.get("note"),
            created_at=created_at,
            updated_at=updated_at,
        )

    @staticmethod
    def _parse_timestamp(
        timestamp: Optional[Any], default: Optional[datetime] = None
    ) -> datetime:
        if timestamp is None:
            return default or datetime.now()

        if isinstance(timestamp, datetime):
            return timestamp

        if isinstance(timestamp, str):
            try:
                return datetime.fromisoformat(timestamp)
            except ValueError:
                return default or datetime.now()

        return default or datetime.now()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, PasswordEntry):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def update_timestamp(self) -> None:
        self.updated_at = datetime.now()

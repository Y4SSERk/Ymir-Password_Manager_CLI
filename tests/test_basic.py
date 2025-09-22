from ymir.core.models.password_entry import PasswordEntry
from ymir.core.models.search_query import SearchQuery
from ymir.core.services.search_service import SearchService
from ymir.core.services.tag_service import TagService


def test_password_entry_creation():
    """Test that we can create a basic PasswordEntry."""
    entry = PasswordEntry(
        service="example.com", username="testuser", password="testpass123"
    )

    assert entry.service == "example.com"
    assert entry.username == "testuser"
    assert entry.password == "testpass123"
    assert entry.id is not None


def test_password_entry_with_tags():
    """Test PasswordEntry with tags."""
    entry = PasswordEntry(
        service="gmail.com", username="user@gmail.com", password="pass123"
    )

    # Test adding tags via TagService
    TagService.add_tag(entry, "work")
    TagService.add_tag(entry, "email")

    assert TagService.has_tag(entry, "work")
    assert TagService.has_tag(entry, "email")
    assert not TagService.has_tag(entry, "personal")


def test_search_query_creation():
    """Test that we can create SearchQuery objects."""
    query = SearchQuery(service="gmail.com")
    assert query.service == "gmail.com"
    assert query.is_empty() is False

    empty_query = SearchQuery()
    assert empty_query.is_empty() is True


def test_search_service_basic():
    """Test basic search functionality."""
    entries = [
        PasswordEntry("gmail.com", "user1", "pass1"),
        PasswordEntry("github.com", "user2", "pass2"),
    ]

    service = SearchService(entries)

    # Test empty query returns all
    results = service.search(SearchQuery())
    assert len(results) == 2

    # Test service search
    results = service.search(SearchQuery(service="gmail.com"))
    assert len(results) == 1
    assert results[0].service == "gmail.com"


def test_tag_search():
    """Test searching by tags."""
    entry1 = PasswordEntry("gmail.com", "user1", "pass1")
    entry2 = PasswordEntry("github.com", "user2", "pass2")

    TagService.add_tag(entry1, "work")
    TagService.add_tag(entry2, "personal")

    service = SearchService([entry1, entry2])

    # Search for work tag
    results = service.search(SearchQuery(tags=["work"]))
    assert len(results) == 1
    assert results[0].service == "gmail.com"


def test_serialization():
    """Test that PasswordEntry can be serialized to dict and back."""
    original = PasswordEntry(
        service="test.com", username="user", password="pass", note="test note"
    )
    TagService.add_tag(original, "test")

    # Convert to dict
    data = original.to_dict()
    assert "id" in data
    assert "service" in data
    assert "tags" in data

    # Convert back from dict
    restored = PasswordEntry.from_dict(data)
    assert restored.service == original.service
    assert restored.username == original.username
    assert "test" in restored.tags

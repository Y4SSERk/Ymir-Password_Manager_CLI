"""Tests for search functionality."""

from ymir.core.search_query import PasswordSearcher, SearchQuery, find_duplicate_entries

from ymir.core.models.password_entry import PasswordEntry


def test_search_query_basic():
    """Test basic search query functionality."""
    entry = PasswordEntry(
        service="Gmail",
        username="user@gmail.com",
        password="test123",
        note="Personal email",
    )

    # Test service search
    query = SearchQuery("gmail", search_fields=["service"], case_sensitive=False)
    assert query.matches(entry) is True

    # Test case sensitive search
    query_case = SearchQuery("gmail", search_fields=["service"], case_sensitive=True)
    assert query_case.matches(entry) is False


def test_password_searcher():
    """Test PasswordSearcher class."""
    entries = [
        PasswordEntry("Gmail", "user1@gmail.com", "pass1", note="work"),
        PasswordEntry("GitHub", "user2", "pass2", note="personal"),
        PasswordEntry("Amazon", "user1@gmail.com", "pass3", note="shopping"),
    ]

    searcher = PasswordSearcher(entries)

    # Search by service
    results = searcher.search_by_service("gmail")
    assert len(results) == 1
    assert results[0].service == "Gmail"

    # Search by username
    results = searcher.search_by_username("user1")
    assert len(results) == 2


def test_duplicate_finder():
    """Test duplicate entry detection."""
    entries = [
        PasswordEntry("Gmail", "user1@gmail.com", "pass1"),
        PasswordEntry("Gmail", "user1@gmail.com", "pass2"),  # Duplicate
        PasswordEntry("GitHub", "user1", "pass3"),
    ]

    duplicates = find_duplicate_entries(entries)
    assert len(duplicates) == 1
    assert len(duplicates[0]) == 2

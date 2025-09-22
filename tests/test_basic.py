"""Basic tests for the password manager."""


def test_placeholder():
    """Placeholder test to ensure CI pipeline works."""
    assert True


def test_imports():
    """Test that main modules can be imported."""
    # Test that modules can be imported without errors
    import ymir.core.models.password_entry

    assert ymir.core.models.password_entry is not None


def test_password_entry_creation():
    """Test basic PasswordEntry functionality."""
    from datetime import datetime

    from ymir.core.models.password_entry import PasswordEntry

    # Test creating a basic entry
    entry = PasswordEntry(
        service="example.com", username="testuser", password="testpass123"
    )

    assert entry.service == "example.com"
    assert entry.username == "testuser"
    assert entry.password == "testpass123"
    assert isinstance(entry.created_at, datetime)

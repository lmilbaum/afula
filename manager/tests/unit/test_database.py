"""
Unit tests for the database module.

Tests:
- Environment variables are read correctly.
- SQLAlchemy engine is created with the expected URL.
- init_db() calls metadata.create_all() as expected.

Author: Liora Milbaum
"""

from unittest import mock

from manager import database


def test_environment_variables(monkeypatch):
    """Test that the environment variables are loaded correctly."""
    monkeypatch.setenv("POSTGRES_HOST", "localhost")
    monkeypatch.setenv("POSTGRES_DB", "test_db")
    monkeypatch.setenv("POSTGRES_USER", "test_user")
    monkeypatch.setenv("POSTGRES_PASSWORD", "test_pass")

    # Reload the module to re-read env vars
    import importlib

    importlib.reload(database)

    assert database.DB_HOST == "localhost"
    assert database.DB_NAME == "test_db"
    assert database.DB_USER == "test_user"
    assert database.DB_PASS == "test_pass"


def test_engine_creation(monkeypatch):
    """Test that the SQLAlchemy engine is created with the correct URL."""
    monkeypatch.setenv("POSTGRES_HOST", "db_host")
    monkeypatch.setenv("POSTGRES_DB", "mydb")
    monkeypatch.setenv("POSTGRES_USER", "myuser")
    monkeypatch.setenv("POSTGRES_PASSWORD", "mypass")

    # Patch create_engine to verify call
    with mock.patch("sqlalchemy.create_engine") as mock_create_engine:
        import importlib

        importlib.reload(database)

        expected_url = "postgresql://myuser:mypass@db_host:5432/mydb"
        mock_create_engine.assert_called_with(expected_url, echo=True)


def test_init_db_calls_create_all():
    """Test that init_db() calls Base.metadata.create_all()."""
    with mock.patch.object(database.Base.metadata, "create_all") as mock_create_all:
        database.init_db()
        mock_create_all.assert_called_once_with(database.engine)

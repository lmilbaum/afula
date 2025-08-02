"""
Shared pytest configuration and fixtures.

This file automatically applies mocks to external dependencies for all tests
in the suite, preventing side effects during import or execution.
"""

import pytest
from manager import main


@pytest.fixture()
def app():
    """Create and configure a new app instance for each test."""
    main.app = main.create_app()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.app_context():
        # Real engine, real tables
        from manager.database import Base, engine

        Base.metadata.create_all(bind=engine)

    yield app

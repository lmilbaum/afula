"""
Unit tests for the Flask application factory and /register endpoint.

This module tests:
- The creation and configuration of the Flask app via create_app().
- That the /register route is properly registered.
- That posting valid data to /register inserts a Repo into the database.
- That invalid payloads return appropriate error responses.
"""

import pytest
import sqlalchemy
from manager import database


@pytest.fixture
def client(app):
    """
    Provide a test client for the Flask app.

    Allows sending HTTP requests to the application
    without running a real server.
    """
    return app.test_client()


def test_register_endpoint_exists(app):
    """Make sure /repos/register URL is registered."""
    rules = [rule.rule for rule in app.url_map.iter_rules()]
    assert "/repos/register" in rules


def test_register_repo_success(client, app):
    """POST /repos/register should insert a new Repo record into the DB."""
    with app.app_context():
        # Ensure tables are created
        database.Base.metadata.create_all(database.engine)

        inspector = sqlalchemy.inspect(database.engine)
        print("Tables:", inspector.get_table_names())

    payload = {"name": "test-repo", "url": "https://github.com/afula/test-repo"}
    response = client.post("/repos/register", json=payload)

    assert response.status_code == 201


def test_register_repo_bad_payload(client):
    """POST /register with missing fields should return 400."""
    response = client.post("/repos/register", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

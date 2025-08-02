"""
Provide and configure the SQLAlchemy database extension.

This module initializes the global `db` instance using Flask‑SQLAlchemy.

Author: Liora Milbaum
"""

import os

import flask_sqlalchemy
import sqlalchemy
from sqlalchemy.orm import declarative_base

db = flask_sqlalchemy.SQLAlchemy()
DB_HOST = os.environ.get("POSTGRES_HOST")
DB_NAME = os.environ.get("POSTGRES_DB")
DB_USER = os.environ.get("POSTGRES_USER")
DB_PASS = os.environ.get("POSTGRES_PASSWORD")

engine = sqlalchemy.create_engine(
    f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}", echo=True
)

Base = declarative_base()


def init_db():
    """Initialize DB."""
    Base.metadata.create_all(engine)

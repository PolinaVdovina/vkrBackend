from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from .flask import get_flask_app

_database = None  # type: SQLAlchemy

Base = declarative_base()
metadata = Base.metadata


def get_database() -> SQLAlchemy:
    global _database
    if not _database:
        _database = SQLAlchemy(app=get_flask_app())
    return _database


def get_database_session() -> Session:
    return get_database().session


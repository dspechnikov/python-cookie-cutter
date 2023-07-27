"""Base sqlalchemy entities."""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

from {{cookiecutter.__project_slug}}.settings import settings

db_engine = create_engine(
    url=settings.database_url,
)


class BaseModel(DeclarativeBase):
    """Base sqlalchemy model."""

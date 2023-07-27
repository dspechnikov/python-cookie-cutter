"""Application settings."""
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Production application settings from environment."""
{% if cookiecutter.orm == 'SQLAlchemy' %}
    database_url: str
{%- endif %}

    class Config:
        """Pydantic settings configuration."""

        env_file = ".env"
        env_prefix = "{{ cookiecutter.__project_slug | upper }}_"


settings = Settings()

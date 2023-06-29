from pydantic import BaseSettings


class Settings(BaseSettings):
    {%- if cookiecutter.orm == 'SQLAlchemy' %}
    database_url: str
    {%- endif %}

    class Config:
        env_file = ".env"


settings = Settings()

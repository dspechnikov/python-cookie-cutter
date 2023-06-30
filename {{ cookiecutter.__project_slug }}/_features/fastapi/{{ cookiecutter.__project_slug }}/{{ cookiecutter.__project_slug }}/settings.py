from pydantic import BaseSettings


class Settings(BaseSettings):
    {%- if cookiecutter.orm == 'SQLAlchemy' %}
    database_url: str
    {%- endif %}

    class Config:
        env_file = ".env"
        env_prefix = "{{ cookiecutter.__project_slug | upper }}_"


settings = Settings()

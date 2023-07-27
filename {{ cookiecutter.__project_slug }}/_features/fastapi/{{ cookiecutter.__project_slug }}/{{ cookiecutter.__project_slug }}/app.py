"""FastAPI application configuration."""
from fastapi import FastAPI

from {{ cookiecutter.__project_slug }}.api.routes import router
{%- if cookiecutter.orm == 'SQLAlchemy' %}
from {{ cookiecutter.__project_slug }}.database.session import DBSessionMiddleware
{%- endif %}

app = FastAPI()
{% if cookiecutter.orm == 'SQLAlchemy' %}
app.add_middleware(DBSessionMiddleware)
{%- endif %}

app.include_router(router)

"""SQLAlchemy session handling."""
from sqlalchemy import orm
from sqlalchemy.orm import sessionmaker
{%- if cookiecutter.web_framework == 'FastAPI' %}
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
{%- endif %}

from {{cookiecutter.__project_slug}}.database.base import db_engine

# expire_on_commit=False to prevent separate DB transactions
# for created object attribute lookup. without that we would need to assign
# each created object to separate variables to use them after commit,
# for example, obj_id = obj.id or obj_not_in_session = obj
Session = sessionmaker(bind=db_engine, future=True, expire_on_commit=False)

{% if cookiecutter.web_framework == 'FastAPI' %}
class DBSessionMiddleware(BaseHTTPMiddleware):
    """A FastAPI middleware for integration with SQLAlchemy session."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint,
    ) -> Response:
        """Add SQLAlchemy session to FastAPI request."""
        request.state.db = Session()
        try:
            response = await call_next(request)
        finally:
            request.state.db.close()

        return response


def db_session(request: Request) -> orm.Session:
    """Wrap request session in a callable to use with fastapi.Depends."""
    if not isinstance(request.state.db, orm.Session):
        raise TypeError(f"Invalid type for request.state.db={request.state.db!r}")
    return request.state.db
{%- endif %}

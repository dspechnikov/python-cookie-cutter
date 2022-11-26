import pytest
from starlette.testclient import TestClient
from {{cookiecutter.__project_slug}}.app import app


@pytest.fixture
def app_client(request):
    client = TestClient(app)
    if getattr(request, "cls", None):
        request.cls.app_client = client

    return client

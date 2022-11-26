from http import HTTPStatus

import pytest


@pytest.mark.usefixtures("app_client")
class TestURLManageRoutes:
    def test_get_something(self):
        response = self.app_client.get(
            "/api/something",
        )

        assert response.status_code == HTTPStatus.OK

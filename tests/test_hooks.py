import os

import pytest
from cookiecutter.utils import work_in

from tests.conftest import run_command


@pytest.mark.usefixtures("render_project_dir")
class TestPostGenProject:
    def test_structure(self, render_project_dir):
        assert render_project_dir.exists()
        assert (render_project_dir / "Pipfile").exists()

    def test_virtualenv_created(self, render_project_dir):
        with work_in(render_project_dir):
            run_command(
                "pipenv --venv",
                env={
                    **os.environ,
                    "PIPENV_VENV_IN_PROJECT": "1",
                    "PIPENV_IGNORE_VIRTUALENVS": "1",
                },
            )

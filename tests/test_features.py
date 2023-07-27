import os
from pathlib import Path

import pytest
from cookiecutter.utils import work_in

from tests.conftest import run_command


@pytest.mark.usefixtures("render_project_dir")
class TestDirectories:
    @pytest.mark.parametrize(
        "render_project_dir, expected_dir",
        [
            (
                {
                    "context": {"ci_platform": "GitHub Actions"},
                },
                Path(".github/workflows"),
            ),
            (
                {
                    "context": {"ci_platform": "GitLab CI"},
                },
                ".gitlab-ci.yml",
            ),
        ],
        indirect=["render_project_dir"],
    )
    def test_root_directory(self, render_project_dir, expected_dir):
        assert (render_project_dir / expected_dir).exists()

    @pytest.mark.parametrize(
        "render_project_dir, expected_dir",
        [
            (
                {
                    "context": {"orm": "SQLAlchemy"},
                },
                "database",
            ),
            (
                {
                    "context": {"web_framework": "FastAPI"},
                },
                "api",
            ),
        ],
        indirect=["render_project_dir"],
    )
    def test_code_directory(self, render_project_dir, expected_dir):
        """
        Test code directories exist. It's a separate test because code directory
        name is dynamic and cannot be accessed inside test parameters.
        """
        assert (render_project_dir / render_project_dir.name / expected_dir).exists()


@pytest.mark.parametrize(
    "render_project_dir",
    [
        {
            "context": {"web_framework": "FastAPI"},
        },
    ],
    indirect=True,
)
@pytest.mark.usefixtures("render_project_dir")
class TestFastAPIFeature:
    def test_unit_tests_run(self, render_project_dir):
        with work_in(render_project_dir):
            run_command(
                "pipenv run test",
                env={
                    **os.environ,
                    "PIPENV_VENV_IN_PROJECT": "1",
                    "PIPENV_IGNORE_VIRTUALENVS": "1",
                },
            )

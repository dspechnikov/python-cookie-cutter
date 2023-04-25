import os
from pathlib import Path

import pytest
from cookiecutter.utils import work_in

from tests.conftest import run_command


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
@pytest.mark.usefixtures("render_project_dir")
class TestGitHubActionsFeature:
    def test_workflows_directory(self, render_project_dir, expected_dir):
        assert (render_project_dir / expected_dir).exists()


@pytest.mark.parametrize(
    "render_project_dir",
    [
        {
            "context": {"web_framework": "FastAPI"},
        }
    ],
    indirect=True,
)
@pytest.mark.usefixtures("render_project_dir")
class TestFastAPIFeature:
    def test_app_structure(self, render_project_dir):
        source_code_dir = render_project_dir / render_project_dir.name
        assert (source_code_dir / "api").exists()
        assert (source_code_dir / "app.py").exists()

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

#!/usr/bin/env python3

import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path
from string import Template

TEMPLATE_REPO_URL = "https://github.com/dspechnikov/python-cookie-cutter"
DEFAULT_PROJECT_NAME = "python_template"
DEFAULT_PYTHON_VERSION = "3.10"
BASE_DIR = Path(os.getcwd())
GITHUB_WORKFLOWS_DIR = Path(".github/workflows")
TEMPLATES_DIR_NAME = "templates"

PYTHON_VERSION_TEMPLATES = (
    ("Pipfile.tpl", "Pipfile"),
    (".pre-commit-config.yaml.tpl", ".pre-commit-config.yaml"),
    ("production.yml.tpl", Path(".github/workflows") / "production.yml"),
    ("staging.yml.tpl", Path(".github/workflows") / "staging.yml"),
)
SRC_DIR_TEMPLATES = ((".coveragerc.tpl", ".coveragerc"),)


def render_template(template_path, context: dict, out_path=None):
    template_dir = Path(template_path).parent

    with open(template_path) as template_file:
        template = Template(template_file.read())

    out_file_path = out_path or template_dir / Path(template_path).name.replace(
        ".tpl", ""
    )
    with open(out_file_path, "w") as out_file:
        out_file.write(template.substitute(**context))


def run_cmd(cmd: str, env=None) -> None:
    subprocess.run(shlex.split(cmd), env=env, check=True)


def main() -> None:
    project_name = (
        input(f"Project name ({DEFAULT_PROJECT_NAME}):") or DEFAULT_PROJECT_NAME
    )
    python_version = (
        input(f"Python version ({DEFAULT_PYTHON_VERSION}):") or DEFAULT_PYTHON_VERSION
    )

    project_dir = BASE_DIR / project_name
    templates_dir = project_dir / TEMPLATES_DIR_NAME

    # clone the repo
    run_cmd(f"git clone {TEMPLATE_REPO_URL} {project_name}")

    # prepare directory structure
    os.rename(project_dir / "src", project_dir / project_name)
    (project_dir / GITHUB_WORKFLOWS_DIR).mkdir(parents=True, exist_ok=True)

    os.chdir(project_dir)

    # create config files
    for template, out_path in PYTHON_VERSION_TEMPLATES:
        render_template(
            templates_dir / template,
            context={"python_version": python_version},
            out_path=out_path,
        )

    for template, out_path in SRC_DIR_TEMPLATES:
        render_template(
            templates_dir / template,
            context={"src_dir": project_name},
            out_path=out_path,
        )

    shutil.rmtree(templates_dir)

    # install dependencies
    run_cmd(
        "pipenv install -d",
        env={
            **os.environ,
            "PIPENV_VENV_IN_PROJECT": "1",
            "PIPENV_IGNORE_VIRTUALENVS": "1",
        },
    )

    # install pre-commit hooks
    run_cmd("pre-commit install")


if __name__ == "__main__":
    sys.exit(main())

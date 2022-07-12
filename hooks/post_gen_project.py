import json
import os
import shlex
import shutil
import subprocess
import sys

# fmt: off
COOKIECUTTER_CONTEXT = json.loads('{{ cookiecutter|tojson }}')
# fmt: on


def run_cmd(cmd: str, env=None) -> None:
    subprocess.run(shlex.split(cmd), env=env, check=True)


def main():
    for feature, path_choices in COOKIECUTTER_CONTEXT["_path_choices"].items():
        if feature not in COOKIECUTTER_CONTEXT:
            raise KeyError(f"{feature=} not found in {COOKIECUTTER_CONTEXT=}")

        paths_to_remove = [
            path_choices[choice]
            for choice in path_choices
            if choice != COOKIECUTTER_CONTEXT[feature]
        ]
        for path in paths_to_remove:
            shutil.rmtree(path)

    run_cmd(
        "pipenv install -d",
        env={
            **os.environ,
            "PIPENV_VENV_IN_PROJECT": "1",
            "PIPENV_IGNORE_VIRTUALENVS": "1",
        },
    )

    run_cmd("git init")

    run_cmd(
        "pipenv run pre-commit install --install-hooks",
        env={
            **os.environ,
            "PIPENV_VENV_IN_PROJECT": "1",
            "PIPENV_IGNORE_VIRTUALENVS": "1",
        },
    )


if __name__ == "__main__":
    sys.exit(main())

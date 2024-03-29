# noqa: INP001 cookiecutter uses hooks directly, no need for a package
"""Cookiecutter post-generation hook."""
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

# black and ruff would use double quotes, it would give error on json.loads call because
# cookiecutter.json content also has double quotes
# fmt: off
COOKIECUTTER_CONTEXT = json.loads('{{ cookiecutter|tojson }}')  # noqa: Q000
# fmt: on


def run_command(cmd: str, env: dict | None = None):
    """Run a shell command."""
    # the function is used only in hook, so ignore bandit warning about untrusted input
    subprocess.run(shlex.split(cmd), env=env, check=True)  # noqa: S603


def render_features():
    """
    Render files required for user-chosen features.

    Conditions for feature to be rendered:
        - feature name must be present in `_features` list in cookiecutter.json
        - feature directory with required files must be placed in `features` directory
          un project root
        - feature directory name must be snake_case version of the user-chosen value
    """
    # no features listed, nothing to render
    if "_features" not in COOKIECUTTER_CONTEXT:
        return

    features_path = Path.cwd() / "_features"
    feature_dirs = os.listdir(features_path)

    for feature_name in COOKIECUTTER_CONTEXT["_features"]:
        if feature_name not in COOKIECUTTER_CONTEXT:
            raise KeyError(
                f"{feature_name=} must be present in {COOKIECUTTER_CONTEXT=}",
            )

        if COOKIECUTTER_CONTEXT[feature_name] is None:
            continue

        # use snake_case version of user choice to avoid having directories with spaces
        # or having to hardcode directory names in cookiecutter.json
        feature_value = re.sub(
            r"[-/\s\\]",
            "_",
            COOKIECUTTER_CONTEXT[feature_name],
        ).lower()

        if feature_value not in feature_dirs:
            raise FileNotFoundError(
                f"{feature_value} directory must be present in {features_path=}",
            )

        shutil.copytree(
            src=features_path / feature_value,
            dst=COOKIECUTTER_CONTEXT["_output_dir"],
            dirs_exist_ok=True,
        )

    shutil.rmtree(features_path)


def main():
    """Wrap hook operations in a function to use with sys.exit."""
    render_features()

    run_command("git init")
    run_command(
        "pipenv install -d",
        env={
            **os.environ,
            "PIPENV_VENV_IN_PROJECT": "1",
            "PIPENV_IGNORE_VIRTUALENVS": "1",
        },
    )
    run_command("cp .env.template .env")


if __name__ == "__main__":
    sys.exit(main())

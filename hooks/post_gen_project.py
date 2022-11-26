import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Optional

from cookiecutter.config import get_user_config
from cookiecutter.generate import generate_files
from cookiecutter.repository import is_repo_url

# black would use double quotes, it would give error on json.loads call because
# cookiecutter.json content also has double quotes
# fmt: off
COOKIECUTTER_CONTEXT = json.loads('{{ cookiecutter|tojson }}')
# fmt: on


def run_command(cmd: str, env: Optional[dict] = None):
    """
    Run a shell command.
    """
    subprocess.run(shlex.split(cmd), env=env, check=True)


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

    if is_repo_url(COOKIECUTTER_CONTEXT["_template"]):
        cookiecutter_config = get_user_config(default_config=True)
        template_name = COOKIECUTTER_CONTEXT["_template"].split("/")[-1]
        cookiecutter_template_path = (
            Path(cookiecutter_config["cookiecutters_dir"]) / template_name
        )
    else:
        cookiecutter_template_path = Path(COOKIECUTTER_CONTEXT["_template"])

    features_path = cookiecutter_template_path / "features"
    feature_dirs = os.listdir(features_path)

    for feature_name in COOKIECUTTER_CONTEXT["_features"]:
        if feature_name not in COOKIECUTTER_CONTEXT:
            raise KeyError(
                f"{feature_name=} must be present in {COOKIECUTTER_CONTEXT=}"
            )

        if COOKIECUTTER_CONTEXT[feature_name] is None:
            continue

        # use snake_case version of user choice to avoid having directories with spaces
        # or having to hardcode directory names in cookiecutter.json
        feature_value = re.sub(
            r"[-/\s\\]", "_", COOKIECUTTER_CONTEXT[feature_name]
        ).lower()

        if feature_value not in feature_dirs:
            raise FileNotFoundError(
                f"{feature_value} directory must be present in {features_path=}"
            )

        generate_files(
            repo_dir=features_path / feature_value,
            context={"cookiecutter": COOKIECUTTER_CONTEXT},
            output_dir=COOKIECUTTER_CONTEXT["_output_dir"],
            accept_hooks=False,
            overwrite_if_exists=True,
        )


def main():
    render_features()

    run_command("git init")

    run_command(
        "pipenv run setup",
        env={
            **os.environ,
            "PIPENV_VENV_IN_PROJECT": "1",
            "PIPENV_IGNORE_VIRTUALENVS": "1",
        },
    )


if __name__ == "__main__":
    sys.exit(main())

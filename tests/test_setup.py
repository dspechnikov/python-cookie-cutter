import os
import shlex
import subprocess
from pathlib import Path

from cookiecutter.main import cookiecutter


def run_cmd(cmd: str, env=None) -> None:
    subprocess.run(shlex.split(cmd), env=env, check=True)


def test_setup():
    cookiecutter(".", no_input=True, overwrite_if_exists=True)

    assert (Path(os.getcwd()) / "python_template").exists()

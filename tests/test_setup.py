import os
from pathlib import Path

from cookiecutter.main import cookiecutter


def test_setup():
    cookiecutter(".", no_input=True, overwrite_if_exists=True)

    assert (Path(os.getcwd()) / "python_template").exists()

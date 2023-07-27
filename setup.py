#!/usr/bin/env python
"""An installation script to generate project template."""
import shlex
import subprocess
import sys

TEMPLATE_REPO_URL = "https://github.com/dspechnikov/python-cookie-cutter"


def run_command(cmd: str, env: dict | None = None):
    """Run a shell command."""
    # the function is used only in script. ignore bandit warning about untrusted input
    subprocess.run(shlex.split(cmd), env=env, check=True)  # noqa: S603


def main():
    """Wrap script commands in a function to use with sys.exit."""
    run_command("python3 -m pip install -q pipenv cookiecutter~=2.1")
    run_command(f"cookiecutter {TEMPLATE_REPO_URL}")
    run_command("python3 -m pip uninstall -y -q cookiecutter")


if __name__ == "__main__":
    sys.exit(main())

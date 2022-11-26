import shlex
import subprocess
import sys
from typing import Optional

TEMPLATE_REPO_URL = "https://github.com/dspechnikov/python-cookie-cutter"


def run_command(cmd: str, env: Optional[dict] = None):
    """
    Run a shell command.
    """
    subprocess.run(shlex.split(cmd), env=env, check=True)


def main():
    run_command("python3 -m pip install -q pipenv cookiecutter~=2.1")
    # force default config to prevent user config from breaking
    # features rendering in post-generate hook
    run_command(f"cookiecutter --default-config {TEMPLATE_REPO_URL}")

    run_command("python3 -m pip uninstall -y -q cookiecutter")


if __name__ == "__main__":
    sys.exit(main())

import shlex
import subprocess
import sys

TEMPLATE_REPO_URL = "https://github.com/dspechnikov/python-cookie-cutter"


def run_cmd(cmd: str, env=None) -> None:
    subprocess.run(shlex.split(cmd), env=env, check=True)


def main() -> None:
    run_cmd("pip install -q pipenv cookiecutter")
    run_cmd(f"cookiecutter {TEMPLATE_REPO_URL}")


if __name__ == "__main__":
    sys.exit(main())

import shlex
import shutil
import subprocess
from pathlib import Path
from typing import Optional

import pytest
from cookiecutter.main import cookiecutter


@pytest.fixture(scope="session")
def render_project_dir(request):
    params = getattr(request, "param", {})
    assert isinstance(params, dict), "must be parametrized with dict of kwargs"
    use_hooks = params.get("use_hooks", True)
    context = params.get("context", {})
    # pin test project version to python version of the root project, so it
    # could be generated on CI
    context.update({"python_version": "3.10"})

    current_dir = Path(__file__).parent
    result_dir = None
    try:
        yield (
            result_dir := Path(
                cookiecutter(
                    template=str(current_dir.parent),
                    no_input=True,
                    overwrite_if_exists=True,
                    accept_hooks=use_hooks,
                    output_dir=current_dir,
                    extra_context=context or {},
                )
            )
        )
    finally:
        shutil.rmtree(result_dir)


def run_command(cmd: str, env: Optional[dict] = None) -> None:
    """
    Run a shell command.
    """
    subprocess.run(shlex.split(cmd), env=env, check=True)

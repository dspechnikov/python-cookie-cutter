import shutil
from pathlib import Path

from cookiecutter.main import cookiecutter


def test_setup():
    current_dir = Path(__file__).parent
    out_path = current_dir / "python_template"

    cookiecutter(
        template=str(current_dir.parent),
        no_input=True,
        overwrite_if_exists=True,
        accept_hooks=False,
        output_dir=out_path,
    )

    assert out_path.exists()

    shutil.rmtree(out_path)

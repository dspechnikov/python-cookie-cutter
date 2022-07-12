import shutil
from pathlib import Path

from cookiecutter.main import cookiecutter


def test_setup():
    current_dir = Path(__file__).parent

    cookiecutter(
        template=str(current_dir.parent),
        no_input=True,
        overwrite_if_exists=True,
        accept_hooks=True,
        output_dir=current_dir,
    )

    out_path = current_dir / "python_template"
    assert out_path.exists()
    assert (out_path / ".git" / "hooks" / "pre-commit").exists()

    shutil.rmtree(out_path)

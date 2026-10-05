"""Every tracked Python file must be valid Python.

ui/app.py once contained a line break inside an f-string (an escape sequence that had become a real newline), so the Streamlit UI could not even be imported;
nothing noticed because CI did not run on pushes. This guard parses every tracked file, so a corrupted file fails here, not in production."""
import ast
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _tracked_python_files():
    out = subprocess.run(["git", "ls-files", "*.py"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.split()
    return [ROOT / f for f in out]


def test_every_tracked_python_file_compiles():
    bad = []
    for path in _tracked_python_files():
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as exc:
            bad.append(f"{path.relative_to(ROOT)}:{exc.lineno} {exc.msg}")
    assert not bad, "files that cannot be compiled: " + "; ".join(bad)

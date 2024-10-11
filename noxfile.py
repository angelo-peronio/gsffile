"""Nox configuration."""

import re

import nox
from nox.sessions import Session

nox.needs_version = ">=2024.3.2"
nox.options.default_venv_backend = "uv"


def version_tuple(version: str) -> tuple[int, ...]:
    """'1.24' --> (1, 24)."""
    return tuple(int(s) for s in version.split("."))


match_classifier = re.compile(
    r"Programming Language :: Python :: (?P<version>\d+\.\d+)"
).match
python_versions = [
    m.group("version")
    for classifier in nox.project.load_toml("pyproject.toml")["project"]["classifiers"]
    if (m := match_classifier(classifier))
]
python_versions.sort(key=version_tuple)

# Only upgrade the PyPy version after NumPy publishes binary wheels
# for the new one, otherwise the CI would take too long.
pypy_versions = ["pypy3.10"]

# For a given NumPy version we support, the latest Python
# with available NumPy binary wheels.
# Keep in sync with dependencies and Python Trove classifiers in pyproject.toml.
numpy_python_versions = (
    ("1.24", "3.11"),
    ("1.25", "3.11"),
    ("1.26", "3.12"),
    ("2.0", "3.12"),
    ("2.1", "3.13"),
)


@nox.session(python=python_versions + pypy_versions)
def test(session: Session) -> None:
    """Test."""
    session.install(".[test]")
    session.run("pytest")


@nox.session()
@nox.parametrize("numpy, python", numpy_python_versions)
def test_numpy(session: Session, numpy: str) -> None:
    """Test the supported NumPy versions."""
    session.install(f"numpy=={numpy}", ".[test]")
    session.run("pytest")


@nox.session(python=python_versions[0])
def test_oldest(session: Session) -> None:
    """Test the oldest supported versions of Python and the dependencies."""
    session.install(f"numpy=={numpy_python_versions[0][0]}", ".[test]")
    session.run("pytest")

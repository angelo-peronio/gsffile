"""Nox configuration."""

import re
from pathlib import Path
from tempfile import gettempdir

import nox
from nox.sessions import Session

nox.needs_version = ">=2024.3.2"
nox.options.default_venv_backend = "uv"
nox.options.envdir = Path(gettempdir()) / "nox"
nox.options.error_on_missing_interpreters = True
nox.options.error_on_external_run = True


def version_tuple(version: str) -> tuple[int, ...]:
    """'1.24' --> (1, 24)."""
    return tuple(int(s) for s in version.split("."))


def get_python_versions() -> list[str]:
    """Extract a sorted list of supported Python versions from the Trove classifiers."""
    classifiers = nox.project.load_toml("pyproject.toml")["project"]["classifiers"]
    match_classifier = re.compile(
        r"Programming Language :: Python :: (?P<version>\d+\.\d+)"
    ).fullmatch
    python_versions = [
        m.group("version")
        for classifier in classifiers
        if (m := match_classifier(classifier))
    ]
    return sorted(python_versions, key=version_tuple)


python_versions = get_python_versions()

# Only upgrade the PyPy version after NumPy publishes binary wheels
# for the new one, otherwise the CI would take too long.
pypy_versions = ["pypy3.10"]

# For each supported NumPy version, the latest Python
# with available NumPy binary wheels.
# Keep in sync with dependencies and Python Trove classifiers in pyproject.toml.
# Keep sorted by ascending NumPy version.
numpy_python_versions = (
    ("1.24", "3.11"),
    ("1.25", "3.11"),
    ("1.26", "3.12"),
    ("2.0", "3.12"),
    ("2.1", "3.13"),
)


@nox.session(python=python_versions + pypy_versions)
def test_python(session: Session) -> None:
    """Test the supported Python versions."""
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


@nox.session()
def coverage(session: Session) -> None:
    """Generate test coverage report."""
    # We generate XML because Codecov would convert it to XML anyway.
    # Coverage analysis slows down the testing, so we do it only once.
    session.install(".[test]")
    session.run("pytest", "--cov=gsffile", "--cov-report=xml")

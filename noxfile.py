"""Nox configuration."""

import re
from pathlib import Path
from tempfile import gettempdir
from typing import Any

import nox
from nox.sessions import Session

nox.needs_version = ">=2024.3.2"
nox.options.default_venv_backend = "uv"
nox.options.envdir = str(Path(gettempdir()) / "nox")
nox.options.error_on_missing_interpreters = True
nox.options.error_on_external_run = True


def version_tuple(version: str) -> tuple[int, ...]:
    """'1.24' --> (1, 24)."""
    return tuple(int(s) for s in version.split("."))


def get_python_versions(pyproject: dict[str, Any]) -> list[str]:
    """Extract a sorted list of supported Python versions from the Trove classifiers."""
    classifiers = pyproject["project"]["classifiers"]
    match_classifier = re.compile(
        r"Programming Language :: Python :: (?P<version>\d+\.\d+)"
    ).fullmatch
    python_versions = [
        m.group("version")
        for classifier in classifiers
        if (m := match_classifier(classifier))
    ]
    return sorted(python_versions, key=version_tuple)


pyproject = nox.project.load_toml("pyproject.toml")
python_versions = get_python_versions(pyproject)
# Only upgrade the PyPy version after NumPy publishes binary wheels
# for the new one, otherwise the CI would take too long.
more_python_versions = ["pypy3.11", "3.13t", "3.14t"]
oldest_deps = [
    spec.replace(">=", "==") for spec in pyproject["project"]["dependencies"]
]


@nox.session(python=python_versions + more_python_versions)
def test_python(session: Session) -> None:
    """Test the supported Python versions."""
    session.install("--group=test", ".")
    session.run("pytest")


@nox.session(python=python_versions[0])
def test_oldest_deps(session: Session) -> None:
    """Test the oldest supported versions of Python and the dependencies."""
    session.install(*oldest_deps, "--group=test", ".")
    session.run("pytest")


@nox.session()
def coverage(session: Session) -> None:
    """Generate test coverage report."""
    # We generate XML because Codecov would convert it to XML anyway.
    # Coverage analysis slows down the testing, so we do it only once.
    session.install("--group=test", ".")
    session.run("pytest", "--cov=gsffile", "--cov-report=xml")

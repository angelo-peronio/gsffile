#!/usr/bin/env -S uv run --script

# /// script
# dependencies = ["nox >= 2025.2.9", "packaging"]
# ///
"""Nox configuration."""

import nox
from nox.project import load_toml as load_pyproject_toml
from nox.project import python_versions as get_python_versions
from nox.sessions import Session
from packaging.version import Version

pyproject = load_pyproject_toml()
# Waiting for nox to take care of sorting.
# https://github.com/wntrblm/nox/issues/1074
python_versions = sorted(get_python_versions(pyproject), key=Version)
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


@nox.session(python=python_versions[-1])  # Use the latest supported Python version.
def coverage(session: Session) -> None:
    """Generate test coverage report."""
    # We generate XML because Codecov would convert it to XML anyway.
    # Coverage analysis slows down the testing, so we do it only once.
    session.install("--group=test", ".")
    session.run("pytest", "--cov=gsffile", "--cov-report=xml")

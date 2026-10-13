#!/usr/bin/env -S uv run --script

# /// script
# dependencies = ["nox >= 2026.08.10"]
# ///
"""Nox configuration."""

import nox
from nox.project import load_toml as load_pyproject_toml
from nox.project import python_versions as get_python_versions
from nox.sessions import Session

# Keep nox.needs_version in sync with:
# * pyproject.toml,
# * the inline metadata above.
nox.needs_version = ">= 2026.08.10"
nox.options.default_venv_backend = "uv"
nox.options.error_on_missing_interpreters = True
nox.options.error_on_external_run = True

pyproject = load_pyproject_toml()
python_versions = get_python_versions(pyproject, sort=True)
# 2026-10-13 Do not test on PyPy, since NumPy >= 2.5 does not publish binary wheels
# for it anymore, see https://github.com/numpy/numpy/issues/30416
# These will be probably published again in the future, see
# https://github.com/numpy/numpy/pull/32332
more_python_versions = ["3.14t", "3.15t"]
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
    session.run("pytest", "--cov=gsffile", "--cov-branch", "--cov-report=xml")


if __name__ == "__main__":
    nox.main()

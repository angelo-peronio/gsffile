"""Nox configuration."""

import nox
from nox.sessions import Session

nox.needs_version = ">=2024.3.2"
nox.options.default_venv_backend = "uv"


@nox.session(python=["3.10", "3.11", "3.12", "3.13"])
def test(session: Session) -> None:
    """Test."""
    session.install(".[test]")
    session.run("pytest")

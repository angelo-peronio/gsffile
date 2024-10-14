"""Test read_gsf."""

from pathlib import Path

import pytest

from gsffile import read_gsf


def test_wrong_magic_line(tmp_path: Path) -> None:
    """Test wrong magic line."""
    content = "Gwyddion Simple Field\nXRes = 1\nYRes = 1\n\x00\x00\x00\x00_¨Ÿ>"
    path = tmp_path / "test.gsf"
    path.write_bytes(bytes(content, encoding="utf-8"))
    with pytest.raises(ValueError, match=r"Magic line not found.*"):
        _ = read_gsf(path)


def test_missing_XRes(tmp_path: Path) -> None:  # noqa: N802
    """Test missing XRes metadata."""
    content = "Gwyddion Simple Field 1.0\nYRes = 1\n\x00\x00\x00\x00_¨Ÿ>"
    path = tmp_path / "test.gsf"
    path.write_bytes(bytes(content, encoding="utf-8"))
    with pytest.raises(KeyError):
        _ = read_gsf(path)


def test_additional_data(tmp_path: Path) -> None:
    """Test additional data at the end of the file."""
    content = (
        "Gwyddion Simple Field 1.0\n"
        "XRes = 1\n"
        "YRes = 1\n"
        "\x00\x00\x00\x00_¨Ÿ>"
        "additional_data"
    )
    path = tmp_path / "test.gsf"
    path.write_bytes(bytes(content, encoding="utf-8"))
    with pytest.raises(ValueError, match=r"Unexpected additional data.*"):
        _ = read_gsf(path)

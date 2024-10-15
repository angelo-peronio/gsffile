"""Test write_gsf."""

from pathlib import Path
from typing import Any

import numpy as np
import pytest

from gsffile.write import write_gsf


def test_wrong_extension(tmp_path: Path) -> None:
    """Test wrong file name extension --> ☠️."""
    data = np.zeros((3, 2), dtype=np.float32)
    with pytest.raises(ValueError, match=r".* .gsf file name extension.*"):
        write_gsf(tmp_path / "test.wrong_extension", data)


wrong_ndim_shapes = [(2, 3, 4), (2, 2, 1), (1, 2, 2), (1, 1, 1, 1), (0, 0, 0)]


@pytest.mark.parametrize("shape", wrong_ndim_shapes, ids=lambda shape: f"shape {shape}")
def test_wrong_ndim(tmp_path: Path, shape: tuple[int]) -> None:
    """Test wrong ndim --> ☠️."""
    data = np.zeros(shape, dtype=np.float32)
    with pytest.raises(ValueError, match=r".* at most 2-dimensional data.*"):
        write_gsf(tmp_path / "test.gsf", data)


def test_wrong_dtype(tmp_path: Path) -> None:
    """Test wrong dtype --> ☠️."""
    data = np.zeros((3, 2), dtype=np.float64)
    with pytest.raises(ValueError, match=r".* only 32-bit floating point data.*"):
        # Ignore unused-ignore to circumvent a (possible) MyPy bug.
        write_gsf(tmp_path / "test.gsf", data)  # type: ignore[arg-type, unused-ignore]


empty_shapes = [(0,), (0, 0), (3, 0), (0, 3)]


@pytest.mark.parametrize("shape", empty_shapes, ids=lambda shape: f"shape {shape}")
def test_empty_array(tmp_path: Path, shape: tuple[int]) -> None:
    """Test empty array --> ☠️."""
    data = np.zeros(shape, dtype=np.float32)
    with pytest.raises(ValueError, match=r".* has 0 elements.*"):
        write_gsf(tmp_path / "test.gsf", data)


@pytest.mark.parametrize(
    "meta", [{"XRes": 101}, {" XRes ": 101}], ids=lambda meta: next(iter(meta.keys()))
)
def test_XRes_in_meta(tmp_path: Path, meta: dict[Any, Any]) -> None:  # noqa: N802
    """Test XRes in meta --> ☠️."""
    data = np.zeros((3, 2), dtype=np.float32)
    with pytest.raises(ValueError, match=r".* neither XRes nor YRes in metadata.*"):
        write_gsf(tmp_path / "test.gsf", data, meta)


@pytest.mark.parametrize(
    "meta", [{"key=key": "value"}, {"key": "="}], ids=lambda meta: str(meta)
)
def test_equal_sign_in_meta(tmp_path: Path, meta: dict[Any, Any]) -> None:
    """Test equal sign in meta --> ☠️."""
    data = np.zeros((3, 2), dtype=np.float32)
    with pytest.raises(ValueError, match=r"Equal sign .*"):
        write_gsf(tmp_path / "test.gsf", data, meta)


@pytest.mark.parametrize(
    "meta",
    [{"key\x00key": "value"}, {"key": "value\x00value"}],
    ids=lambda meta: str(meta),
)
def test_null_char_in_meta(tmp_path: Path, meta: dict[Any, Any]) -> None:
    """Test equal sign in meta --> ☠️."""
    data = np.zeros((3, 2), dtype=np.float32)
    with pytest.raises(ValueError, match=r"Null character .*"):
        write_gsf(tmp_path / "test.gsf", data, meta)

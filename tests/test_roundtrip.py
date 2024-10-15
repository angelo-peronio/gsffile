"""Test that what is read is what we expect, given what was written."""

from pathlib import Path
from typing import Any

import numpy as np
import pytest
from numpy.typing import NDArray

from gsffile import read_gsf, write_gsf
from gsffile.write import prepare_data, prepare_metadata

rng = np.random.default_rng(seed=1)


def assert_roundtrip_ok(
    tmp_path: Path, data: NDArray[np.float32], meta: dict[Any, Any] | None = None
) -> None:
    """Assert that what is read is what we expect, given what was written."""
    path = tmp_path / "test.gsf"
    write_gsf(path, data, meta)
    data_2, meta_2 = read_gsf(path)
    expected_data = prepare_data(data)
    expected_meta = prepare_metadata(meta)
    assert meta_2 == expected_meta
    # Check metadata order.
    assert list(meta_2.keys()) == list(expected_meta.keys())
    np.testing.assert_array_equal(data_2, expected_data)


allowed_shapes = [(3, 2), (3, 1), (1, 3), (3,), (1,), ()]


@pytest.mark.parametrize("shape", allowed_shapes, ids=lambda shape: f"shape {shape}")
def test_allowed_shapes(tmp_path: Path, shape: tuple[int]) -> None:
    """Test 0-, 1-, and 2-dimensional random data."""
    data = rng.uniform(size=shape).astype(np.float32)
    assert_roundtrip_ok(tmp_path, data)


def test_meta(tmp_path: Path) -> None:
    """Test metadata roundtrip."""
    # Optional fields of non-str type, such as XReal, would fail this test.
    data = np.zeros((2, 3), dtype=np.float32)
    meta = {
        "string": "a string",
        "float": np.sqrt(3),
        "int": -0,
        "  whitespace  ": " ",
        "multi-byte characters": "💣",
        "ZUnits": "m",
        "XYUnits": "m",
    }
    assert_roundtrip_ok(tmp_path, data, meta)


def test_non_finite(tmp_path: Path) -> None:
    """Test roundtrip for inf and NaN."""
    data = np.array([[np.inf, -np.inf], [np.nan, -0.0]], dtype=np.float32)
    assert_roundtrip_ok(tmp_path, data)


def test_path_as_str(tmp_path: Path) -> None:
    """Test passing a str as path."""
    data = np.zeros((2, 3), dtype=np.float32)
    path = tmp_path / "test.gsf"
    write_gsf(str(path), data)
    _ = read_gsf(str(path))

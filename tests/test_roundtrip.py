"""Test that what is read is the same that what was written."""

import numpy as np
import pytest

from gsf_file import read_gsf, write_gsf

rng = np.random.default_rng(seed=1)


def expected_data(data):
    """What data to expect after a read_gsf ∘ write_gsf roundtrip."""  # noqa: D401
    return np.atleast_2d(data)


def expected_meta(meta):
    """What metadata to expect after a read_gsf ∘ write_gsf roundtrip."""  # noqa: D401
    if meta is None:
        return {}
    return {str(key).strip(): str(value).strip() for key, value in meta.items()}


def assert_roundtrip_ok(tmp_path, data, meta=None):
    """Assert that what is read is the same that what was written."""
    path = tmp_path / "test.gsf"
    write_gsf(path, data, meta)
    meta_2, data_2 = read_gsf(path)
    assert meta_2 == expected_meta(meta)
    np.testing.assert_array_equal(data_2, expected_data(data))


allowed_shapes = [(3, 2), (3, 1), (1, 3), (3,), (1,), ()]


@pytest.mark.parametrize("shape", allowed_shapes, ids=lambda shape: f"shape {shape}")
def test_allowed_shapes(tmp_path, shape):
    """Test 0-, 1-, and 2-dimensional random data."""
    data = rng.uniform(size=shape).astype(np.float32)
    assert_roundtrip_ok(tmp_path, data)


def test_meta(tmp_path):
    """Test metadata roundtrip."""
    data = np.zeros((2, 3), dtype=np.float32)
    meta = {
        "string": "a string",
        "float": 7.40,
        "int": 2,
        "  whitespace  ": " ",
        "non_ascii_meta": "💣",
    }
    assert_roundtrip_ok(tmp_path, data, meta)

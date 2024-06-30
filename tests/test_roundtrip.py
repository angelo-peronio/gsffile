"""Test that what is read is the same that what was written."""

import numpy as np
import pytest

from gsf_file import read_gsf, write_gsf

allowed_shapes = [(3, 2), (3, 1), (1, 3), (3,), (1,), ()]
not_allowed_shapes = [(3, 3, 1), (1, 3, 3), (1, 1, 1, 1)]


@pytest.mark.parametrize("shape", allowed_shapes, ids=lambda shape: f"shape {shape}")
def test_roundtrip(tmp_path, shape):
    """Test that what is read is the same that what was written."""
    data_1 = np.zeros(shape, dtype=np.float32)
    path = tmp_path / "test.gsf"
    write_gsf(data_1, path)
    meta_2, data_2 = read_gsf(str(path))
    expected_data_1 = np.atleast_2d(data_1)
    assert meta_2 == {}
    np.testing.assert_array_equal(data_2, expected_data_1)

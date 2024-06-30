"""Test write_gsf."""

import numpy as np
import pytest

from gsf_file.write import write_gsf


def test_wrong_extension(tmp_path):
    """Test wrong file name extension --> ☠️."""
    data = np.zeros((3, 3), dtype=np.float32)
    with pytest.raises(ValueError, match=r".* .gsf file name extension.*"):
        write_gsf(data, tmp_path / "test.wrong_extension")


def test_ndim(tmp_path):
    """Test wrong ndim --> ☠️."""
    data = np.zeros((3, 3, 3), dtype=np.float32)
    with pytest.raises(ValueError, match=r".* at most 2-dimensional data.*"):
        write_gsf(data, tmp_path / "test.gsf")


def test_wrong_dtype(tmp_path):
    """Test wrong dtype --> ☠️."""
    data = np.zeros((3, 3), dtype=np.float64)
    with pytest.raises(ValueError, match=r".* only 32-bit floating point data.*"):
        write_gsf(data, tmp_path / "test.gsf")

import numpy as np
from gsf_file import read_gsf, write_gsf


def test_roundtrip(tmp_path):
    image_width_px = 3
    data_1 = np.eye(image_width_px, dtype=np.float32)
    meta_1 = {"XRes": image_width_px, "YRes": image_width_px}
    path = tmp_path / "test.gsf"
    write_gsf(data_1, str(path), meta_1)
    meta_2, data_2 = read_gsf(str(path))
    assert meta_2 == meta_1
    np.testing.assert_array_equal(data_2, data_1)
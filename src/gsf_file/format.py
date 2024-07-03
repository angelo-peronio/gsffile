"""Details of the Gwyddion Simple Field format."""

import numpy as np

null_byte = b"\x00"  # bytes
null_char = null_byte.decode()  # str
gsf_magic_line = "Gwyddion Simple Field 1.0\n"
gsf_known_metadata_types = {
    "XRes": int,
    "YRes": int,
    "XReal": float,
    "YReal": float,
    "XOffset": float,
    "YOffset": float,
    "Title": str,
    "XYUnits": str,
    "ZUnits": str,
}
gsf_known_metadata_order = {
    key: i for i, key in enumerate(gsf_known_metadata_types, start=1)
}
# 32-bit (4-bytes) little-endian floats.
gsf_dtype = np.dtype("<f4")
# Row-major order.
gsf_array_order = "C"


def gsf_padding_lenght(header_length):
    """Length of the null-byte padding between metadata and data."""
    return 4 - header_length % 4

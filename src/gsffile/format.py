"""Details of the Gwyddion Simple Field format."""

from typing import Final

import numpy as np

null_byte: Final[bytes] = b"\x00"
null_char: Final[str] = null_byte.decode()
gsf_magic_line: Final = "Gwyddion Simple Field 1.0\n"
# This cries for a TypedDict, but I have yet to find a sane way to specify "extra"
# (not required, not known in advance) keys.
gsf_known_metadata_types: Final = {
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
gsf_known_metadata_order: Final = {
    key: i for i, key in enumerate(gsf_known_metadata_types, start=1)
}
# 32-bit (4-bytes) little-endian floats.
gsf_dtype: Final = np.dtype("<f4")
# Row-major order.
gsf_array_order: Final = "C"


def gsf_padding_lenght(header_length: int) -> int:
    """Length of the null-byte padding between metadata and data."""
    return 4 - header_length % 4

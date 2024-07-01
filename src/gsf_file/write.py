"""Write Gwyddion Simple Field files."""

from pathlib import Path

import numpy as np

from .format import (
    gsf_dtype,
    gsf_magic_line,
    gsf_order,
    gsf_padding_lenght,
    null_byte,
    null_char,
)


def write_gsf(
    data: np.typing.NDArray[np.float32],
    path: Path | str,
    metadata: dict | None = None,
):
    """Write a NumPy array to a Gwyddion Simple Field file (.gsf).

    Parameters
    ----------
        data
            A 2-dimensional array of float32. 0- and 1-dimensional arrays
            will be reshaped to 2 dimensions.
        path
            path to the output file to be written, with .gsf extension.
        metadata : optional
            additional metadata to be included in the output file.

    Raises
    ------
        ValueError
            If the input parameters are not compatible with the Gwyddion Simple Field
            file format.
    """
    # Support 0- and 1-dimensional data.
    data = np.atleast_2d(data)

    if data.ndim >= 3:
        raise ValueError(
            f"data.shape is {data.shape}, but the Gwyddion Simple Field file format "
            "supports at most 2-dimensional data."
        )
    if data.dtype != np.float32:
        raise ValueError(
            f"data.dtype is {data.dtype}, but the Gwyddion Simple Field file format "
            "supports only 32-bit floating point data. "
            "Convert with data.astype(np.float32)."
        )

    path = Path(path)
    if path.suffix != ".gsf":
        raise ValueError(
            "The Gwyddion Simple Field file format uses the .gsf file name extension."
        )

    if metadata is None:
        metadata = {}
    metadata = {str(key).strip(): str(value).strip() for key, value in metadata.items()}
    if ("XRes" in metadata) or ("YRes" in metadata):
        raise ValueError(
            "Do not specify neither XRes nor YRes in metadata. "
            "They are derived form data.shape."
        )
    for key, value in metadata.items():
        if ("=" in key) or ("=" in value):
            raise ValueError(
                "Equal sign '=' not allowed in metadata. "
                f"Offending key: {key}, offending value: {value}"
            )
        if (null_char in key) or (null_char in value):
            raise ValueError(
                "Null character (ASCII code 0) not allowed in metadata. "
                f"Offending key: {key}, offending value: {value}"
            )
    metadata = {"XRes": data.shape[1], "YRes": data.shape[0]} | metadata

    header = gsf_magic_line
    for key, value in metadata.items():
        header += f"{key} = {value}\n"
    header_bytes = bytes(header, "utf-8")
    gsf_padding = null_byte * gsf_padding_lenght(len(header_bytes))

    with path.open("wb") as file:
        file.write(header_bytes)
        file.write(gsf_padding)
        file.write(data.astype(gsf_dtype).tobytes(order=gsf_order))

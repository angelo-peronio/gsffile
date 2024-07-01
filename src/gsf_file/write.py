"""Write Gwyddion Simple Field files."""

from pathlib import Path

import numpy as np

from .format import (
    gsf_array_order,
    gsf_dtype,
    gsf_magic_line,
    gsf_metadata_order,
    gsf_padding_lenght,
    null_byte,
    null_char,
)


def write_gsf(
    path: Path | str,
    data: np.typing.NDArray[np.float32],
    metadata: dict | None = None,
):
    """Write a NumPy array to a Gwyddion Simple Field file (.gsf).

    Parameters
    ----------
        path
            Path to the output file to be written, with .gsf extension.
        data
            A 2-dimensional array of float32. 0- and 1-dimensional arrays
            will be reshaped to 2 dimensions.
        metadata : optional
            Additional metadata to be included in the output file. The optional fields
            defined by the Gwyddion Simple Field format will be written first, followed
            by the custom fields defined by the user.

    Raises
    ------
        ValueError
            If the input parameters are not compatible with the Gwyddion Simple Field
            file format.
    """
    data = prepare_data(data)
    if data.ndim >= 3:  # noqa: PLR2004
        msg = (
            f"data.shape is {data.shape}, but the Gwyddion Simple Field file format "
            "supports at most 2-dimensional data."
        )
        raise ValueError(msg)
    if data.dtype != np.float32:
        msg = (
            f"data.dtype is {data.dtype}, but the Gwyddion Simple Field file format "
            "supports only 32-bit floating point data. "
            "Convert with data.astype(np.float32)."
        )
        raise ValueError(msg)

    path = Path(path)
    if path.suffix != ".gsf":
        msg = "The Gwyddion Simple Field file format uses the .gsf file name extension."
        raise ValueError(msg)

    metadata = prepare_metadata(metadata)
    if ("XRes" in metadata) or ("YRes" in metadata):
        msg = (
            "Do not specify neither XRes nor YRes in metadata. "
            "They are derived form data.shape."
        )
        raise ValueError(msg)
    for key, value in metadata.items():
        if ("=" in key) or ("=" in value):
            msg = (
                "Equal sign '=' not allowed in metadata. "
                f"Offending key: {key}, offending value: {value}"
            )
            raise ValueError(msg)
        if (null_char in key) or (null_char in value):
            msg = (
                "Null character (ASCII code 0) not allowed in metadata. "
                f"Offending key: {key}, offending value: {value}"
            )
            raise ValueError(msg)
    metadata = {"XRes": data.shape[1], "YRes": data.shape[0]} | metadata

    header = gsf_magic_line
    for key, value in metadata.items():
        header += f"{key} = {value}\n"
    header_bytes = bytes(header, "utf-8")
    gsf_padding = null_byte * gsf_padding_lenght(len(header_bytes))

    with path.open("wb") as file:
        file.write(header_bytes)
        file.write(gsf_padding)
        file.write(data.astype(gsf_dtype).tobytes(order=gsf_array_order))


def prepare_data(data):
    """Reshape 0- and 1-dimensional arrays to 2 diemnsions."""
    return np.atleast_2d(data)


def prepare_metadata(metadata):
    """Sort, convert to string, and strip whitespace from the metadata."""
    if metadata is None:
        metadata = {}
    metadata = dict(
        sorted(metadata.items(), key=lambda item: gsf_metadata_order(item[0]))
    )
    metadata = {str(key).strip(): str(value).strip() for key, value in metadata.items()}
    return metadata  # noqa: RET504

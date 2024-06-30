"""Write Gwyddion Simple Field files."""

from pathlib import Path

import numpy as np


def write_gsf(
    data: np.typing.NDArray[np.float32],
    path: Path | str,
    metadata: dict | None = None,
):
    """Write a NumPy array to a Gwyddion Simple Field file (.gsf).

    Parameters
    ----------
        data
            A 0-, 1-, or 2-dimensional array of float32.
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
    # Support for 0- and 1-dimensional data.
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

    header = ""
    header += "Gwyddion Simple Field 1.0\n"
    header += f"XRes = {data.shape[1]}\n"
    header += f"YRes = {data.shape[0]}\n"
    for key, value in metadata.items():
        header += f"{key} = {value}\n"
    padding_lenght = 4 - len(header) % 4

    with path.open("wb") as file:
        file.write(bytes(header, "utf-8"))
        file.write(b"\x00" * padding_lenght)
        file.write(data.tobytes(None))

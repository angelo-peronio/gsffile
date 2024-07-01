"""Read Gwyddion Simple Field files."""

from contextlib import suppress
from pathlib import Path

import numpy as np

from .format import (
    gsf_dtype,
    gsf_known_metadata_types,
    gsf_magic_line,
    gsf_padding_lenght,
    null_byte,
)


def read_gsf(path: Path | str) -> tuple[dict, np.typing.NDArray[np.float32]]:
    """Read a Gwyddion Simple Field file (.gsf).

    Parameters
    ----------
        path
            Path to the file to be read.

    Returns
    -------
        metadata
        data

    Raises
    ------
        ValueError
            If the file to be read is not a Gwyddion Simple Field.
        KeyError
            If required metadata is missing from the file to be read.
    """
    path = Path(path)
    metadata = {}

    with path.open("rb") as file:
        # Check magic line.
        if file.readline().decode() != gsf_magic_line:
            raise ValueError(f"Magic line not found at the beginning of {path}")

        # Read metadata.
        # Peek does not do what you think it does.
        # https://stackoverflow.com/a/24474743
        while file.peek(1)[:1] != null_byte:
            key, value = file.readline().decode().split("=")
            metadata[key.strip()] = value.strip()
        for key, type_ in gsf_known_metadata_types.items():
            with suppress(KeyError):
                metadata[key] = type_(metadata[key])

        # Skip null-byte padding.
        header_length = file.tell()
        file.seek(gsf_padding_lenght(header_length), 1)

        # Read data.
        shape = metadata["YRes"], metadata["XRes"]
        data_size = gsf_dtype.itemsize * shape[0] * shape[1]
        data = np.frombuffer(file.read(data_size), dtype=gsf_dtype).reshape(shape)

        if file.read(1) != b"":
            raise ValueError(f"Unexpected additional data found at the end of {path}")

    # Do not duplicate information already present in data.shape.
    del metadata["XRes"]
    del metadata["YRes"]

    return metadata, data

"""Read Gwyddion Simple Field files."""

from contextlib import suppress
from pathlib import Path

import numpy as np

from .format import (
    NUL,
    gsf_dtype,
    gsf_known_metadata_types,
    gsf_magic_line,
    gsf_padding_lenght,
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
    """
    path = Path(path)
    metadata = {}

    with path.open("rb") as file:
        # Check magic line.
        if file.readline().decode("utf-8") != gsf_magic_line:
            raise ValueError(f"GSF magic line not found at the beginning of {path}")

        # Read metadata.
        # Peek does not do what you think it does.
        # https://stackoverflow.com/a/24474743
        while file.peek(1)[:1] != NUL:
            key, value = file.readline().decode("utf-8").split("=")
            metadata[key.strip()] = value.strip()
        for key, type_ in gsf_known_metadata_types.items():
            with suppress(KeyError):
                metadata[key] = type_(metadata[key])

        # Skip NUL padding.
        header_length = file.tell()
        file.seek(gsf_padding_lenght(header_length), 1)

        # Read data.
        shape = metadata["YRes"], metadata["XRes"]
        data_size = 4 * shape[0] * shape[1]
        data = np.frombuffer(file.read(data_size), dtype=gsf_dtype).reshape(shape)

        if file.read(1) != b"":
            raise ValueError(f"Unexpected additional data found at the end of {path}")

    # Do not duplicate information already present in data.shape.
    del metadata["XRes"]
    del metadata["YRes"]

    return metadata, data

"""Read Gwyddion Simple Field files."""

import logging
from contextlib import suppress
from pathlib import Path
from typing import Any, cast

import numpy as np
from numpy.typing import NDArray

from .format import (
    gsf_dtype,
    gsf_known_metadata_types,
    gsf_magic_line,
    gsf_padding_lenght,
    null_byte,
)

log = logging.getLogger(__name__)


def read_gsf(
    path: Path | str,
) -> tuple[NDArray[np.float32], dict[str, Any]]:
    """Read a Gwyddion Simple Field file (.gsf).

    Parameters
    ----------
        path
            Path to the file to be read.

    Returns
    -------
        metadata
            A dict of metadata. The fields XRes and YRes are not included,
            since they would be a duplicate of data.shape. Custom fields not mentioned
            in the Gwyddion Simple Field specification are read as strings.
        data
            A 2-dimensional NumPy array of float32.

    Raises
    ------
        ValueError
            If the file to be read is not a Gwyddion Simple Field.
        KeyError
            If required metadata is missing from the file to be read.
    """
    path = Path(path)
    metadata = {}
    log.info("Reading %s", path)

    with path.open("rb") as file:
        # Check magic line.
        if file.readline().decode() != gsf_magic_line:
            msg = f"Magic line not found at the beginning of {path}"
            raise ValueError(msg)

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
        # cast is there to persuade mypy.
        shape = cast("int", metadata["YRes"]), cast("int", metadata["XRes"])
        data_size = gsf_dtype.itemsize * shape[0] * shape[1]
        data = np.frombuffer(file.read(data_size), dtype=gsf_dtype).reshape(shape)

        if file.read(1) != b"":
            msg = f"Unexpected additional data found at the end of {path}"
            raise ValueError(msg)

    log.info(
        "Read an image of width: %s px, height: %s px", data.shape[1], data.shape[0]
    )
    log.debug("Read metadata: %s", metadata)

    # Do not duplicate information already present in data.shape.
    del metadata["XRes"]
    del metadata["YRes"]

    return data, metadata

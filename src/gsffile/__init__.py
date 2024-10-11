"""Read and write Gwyddion Simple Field files (.gsf).

The `Gwyddion Simple Field <http://gwyddion.net/documentation/user-guide-en/gsf.html>`_
file format (.gsf) is a single-channel format for 2D data that was designed to be
easy and efficient to read and write, with human-readable header, reasonably expressive,
and avoiding instrument or application specific fields
(though it can optionally bear them).
"""

from importlib.metadata import version

from .read import read_gsf
from .write import write_gsf

__version__ = version("gsffile")
__all__ = ["read_gsf", "write_gsf"]

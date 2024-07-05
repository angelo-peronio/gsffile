# Read and write Gwyddion Simple Field files

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
![license](https://img.shields.io/github/license/angelo-peronio/gsffile)
![python](https://img.shields.io/pypi/pyversions/gsffile)
![ci](https://github.com/angelo-peronio/gsffile/actions/workflows/ci.yaml/badge.svg)
![pypI](https://img.shields.io/pypi/v/gsffile)

`gsffile` is a Python library to:

* read image and metadata from [Gwyddion Simple Field](http://gwyddion.net/documentation/user-guide-en/gsf.html) (.gsf) files, and
* store NumPy arrays in Gwyddion Simple Field files.

It features type annotations and an extensive test suite.

## Setup

Install with `pip`:

```bash
python -m pip install --upgrade gsffile
```

## Quickstart

```python
from gsffile import read_gsf, write_gsf
import numpy as np

# The Gwyddion Simple Field format supports only 32-bit floating point data.
data = np.eye((100, 100), dtype=np.float32)
# Optional metadata.
metadata = {
    "XReal": 5e-05,
    "YReal": 5e-05,
    "XYUnits": "m",
    "ZUnits": "V",
    "CustomKey": 33,
    }

write_gsf("example.gsf", data, meta)

data, metadata = read_gsf("example.gsf")
```

## Documentation

`gsffile` is documented via docstrings:

```bash
python -c "import gsffile; help(gsffile)"
```

## Roadmap

* [x] Test against Python 3.13 and PyPy
* Publish!
    [x] Register on PyPI
    [ ] Make repo public
    [ ] Tag and push
* [ ] Conda recipe, shield
* [ ] Avoid having to pass `tmp_dir` to tests calling `assert_roundtrip_ok`
* [ ] xarray integration
* [ ] [pre-commit](https://learn.scientific-python.org/development/guides/style/), pre-commit.ci, shield
* [ ] Test workflow to gate pull requests
* [ ] Advertise!
    * [ ] image.sc announcements
    * [ ] Gwyddion mailing list

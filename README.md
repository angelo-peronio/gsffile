# Read and write Gwyddion Simple Field files

[![pypi](https://img.shields.io/pypi/v/gsffile)](https://pypi.org/project/gsffile/)
[![conda-forge](https://img.shields.io/conda/vn/conda-forge/gsffile)](https://anaconda.org/conda-forge/gsffile)
[![python](https://img.shields.io/pypi/pyversions/gsffile)](https://pypi.org/project/gsffile/)
[![license](https://img.shields.io/github/license/angelo-peronio/gsffile?color=2DBA4E)](https://github.com/angelo-peronio/gsffile/blob/master/LICENSE)
[![ci](https://github.com/angelo-peronio/gsffile/actions/workflows/ci.yaml/badge.svg)](https://github.com/angelo-peronio/gsffile/actions/workflows/ci.yaml)
[![codecov](https://codecov.io/github/angelo-peronio/gsffile/graph/badge.svg)](https://codecov.io/github/angelo-peronio/gsffile)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/angelo-peronio/gsffile/master.svg)](https://results.pre-commit.ci/latest/github/angelo-peronio/gsffile/master)
[![ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/format.json)](https://github.com/astral-sh/ruff)

`gsffile` is a Python library to:

* read image and metadata from [Gwyddion Simple Field](http://gwyddion.net/documentation/user-guide-en/gsf.html) (.gsf) files, and
* store NumPy arrays in Gwyddion Simple Field files.

It features type annotations and an overgrown test suite.

## Setup

Install with `pip`

```bash
python -m pip install --upgrade gsffile
```

or with `conda`

```bash
conda install gsffile
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

write_gsf("example.gsf", data, metadata)

data, metadata = read_gsf("example.gsf")
```

## Documentation

`gsffile` is documented via docstrings:

```bash
python -c "import gsffile; help(gsffile)"
```

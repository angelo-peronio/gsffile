# Read and write Gwyddion Simple Field files

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
![license](https://img.shields.io/github/license/angelo-peronio/gsffile)
![test](https://github.com/angelo-peronio/gsffile/actions/workflows/test.yaml/badge.svg)
![build](https://github.com/angelo-peronio/gsffile/actions/workflows/build.yaml/badge.svg)

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

* [ ] CI and publish
    * <https://packaging.python.org/en/latest/guides/using-testpypi/>
    * <https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/>
    * <https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python>
    * <https://github.com/hynek/build-and-inspect-python-package>
    * PyPI shields
* [ ] Conda recipe, shield
* Later
    * [ ] Avoid having to pass `tmp_dir` to tests calling `assert_roundtrip_ok`
    * [ ] xarray integration
    * [ ] [pre-commit](https://learn.scientific-python.org/development/guides/style/), pre-commit.ci, shield
    * [ ] Test against Python 3.13 and PyPy
* [ ] Advertise!

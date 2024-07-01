# Read and write Gwyddion Simple Field files

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
![test](https://img.shields.io/github/actions/workflow/status/angelo-peronio/gsf-file/test.yaml)
![build](https://img.shields.io/github/actions/workflow/status/angelo-peronio/gsf-file/build.yaml)

`gsf_file` is a Python library to read and write [Gwyddion Simple Field](http://gwyddion.net/documentation/user-guide-en/gsf.html) (.gsf) files.

## Example

```python
from gsf_file import read_gsf, write_gsf
import numpy as np

# The Gwyddion Simple Field format supports only 32-bit floating point data.
data = np.eye((100, 100), dtype=np.float32)
# Optional metadata.
meta = {
    "XReal": 5e-05,
    "YReal": 5e-05,
    "XYUnits": "m",
    "ZUnits": "V",
    "CustomKey": 33,
    }
write_gsf(data, "example.gsf", meta)

meta, data = read_gsf("example.gsf")
```

## Roadmap

- [x] Package
- [x] Test
- [x] GitHub
- [x] Ruff
- [x] Modernize code
    - [x] Rework `read_gsf`
    - [x] Ensure little-endian byte ordering
    - [x] Test multi-byte character in metadata
    - [x] Strip whitespace from metadata
    - [x] Check Unix newline
    - [x] Check NUL and = character in header. Validate functions.
    - [x] Test not allowed shapes
    - [x] Peruse specs
    - [x] Check Ruff ignores
- [ ] Docs
    - [ ] Usage
    - [ ] Scripts
    - [ ] Spell check
- [x] Use the same parameter ordering as `imwrite`
- [x] Package name: `gsf_file` or `gsf-file`?
    - <https://discuss.python.org/t/are-there-any-naming-conventions-for-package-names/47746>
    - <https://packaging.python.org/en/latest/specifications/name-normalization/#names-and-normalization>
- [ ] PyPI
- [ ] [Shields](https://shields.io/)
- [ ] [Best practices](https://learn.scientific-python.org/development/guides/packaging-simple/)
- [ ] Continuous integration
- [ ] Auto-versioning
- [ ] Conda recipe
- Later
    - [ ] Avoid having to pass `tmp_dir` to tests calling `assert_roundtrip_ok`
    - [ ] xarray integration
    - [ ] Sort metadata
    - [ ] Check no infinities. Allow NaNs?
- [ ] Advertise, e.g. Gwyddion mailing list and/or forum

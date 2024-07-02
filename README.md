# Read and write Gwyddion Simple Field files

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
![test](https://github.com/angelo-peronio/gsf-file/actions/workflows/test.yaml/badge.svg)
![build](https://github.com/angelo-peronio/gsf-file/actions/workflows/build.yaml/badge.svg)

`gsf-file` is a Python library to read and write [Gwyddion Simple Field](http://gwyddion.net/documentation/user-guide-en/gsf.html) (.gsf) files.

## Example

```python
from gsf_file import read_gsf, write_gsf
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
    - [ ] Readthedocs
    - [ ] Shield
- [x] Use the same parameter ordering as `imwrite`
- [x] Package name: `gsf_file` or `gsf-file`?
    - <https://discuss.python.org/t/are-there-any-naming-conventions-for-package-names/47746>
    - <https://packaging.python.org/en/latest/specifications/name-normalization/#names-and-normalization>
    - <https://groups.google.com/g/comp.lang.python/c/Y5zcSR7wn7c>
    - <https://labdmitriy.github.io/blog/distributions-vs-packages/>
    - Now `gsf-file`, to be re-evalueted before publishing.
    - But the package has an underscore!
- [ ] Publish
    - [ ] <https://packaging.python.org/en/latest/guides/using-testpypi/>
    - [ ] <https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/>
- [x] [Shields](https://shields.io/)
- [x] [Best practices](https://learn.scientific-python.org/development/guides/packaging-simple/)
- [x] Continuous integration
    - [ ] pre-commit <https://learn.scientific-python.org/development/guides/style/>
- [x] Dynamic version
- [ ] Conda recipe
- Later
    - [ ] Avoid having to pass `tmp_dir` to tests calling `assert_roundtrip_ok`
    - [ ] xarray integration
    - [x] Sort metadata
    - [x] Allow infinities and NaNs
- [ ] Advertise, e.g. Gwyddion mailing list and/or forum

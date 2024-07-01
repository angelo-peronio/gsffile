# Read and write Gwyddion Simple Field files

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

`gsf_file` is a Python library to read and write [Gwyddion Simple Field](http://gwyddion.net/documentation/user-guide-en/gsf.html) (.gsf) files.

## Roadmap

- [x] Package
- [x] Test
- [x] GitHub
- [x] Ruff
- [ ] Modernize code
    - [x] Rework `read_gsf`
    - [x] Ensure little-endian byte ordering
    - [x] Test multi-byte character in metadata
    - [x] Strip whitespace from metadata
    - [x] Check Unix newline
    - [x] Check NUL and = character in header. Validate functions.
    - [ ] Check no infinities. Allow NaNs?
    - [x] Test not allowed shapes
    - [ ] Sort metadata?
    - [x] Peruse specs
- [ ] Docs
- [ ] PyPI
- [ ] [Shields](https://shields.io/)
- [ ] [Best practices](https://learn.scientific-python.org/development/guides/packaging-simple/)
- [ ] Continuous integration
- [ ] Auto-versioning
- [ ] Conda recipe
- [ ] Advertise
    - Gwyddion mailing list and/or forum

## Notes

- <https://github.com/pytest-dev/pytest/issues/1830#issuecomment-425653756>

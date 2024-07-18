# Development notes of `gsffile`

## How to release

Push a tag named `v[major].[minor].[patch]`.

## Roadmap

* [x] Code style Ruff shield, see pint
* [ ] coveralls or codecov <https://learn.scientific-python.org/development/guides/coverage/>
* [ ] pre-commit.ci, shield
* [x] Conda recipe, shield
* [ ] Release script
* [ ] Test workflow to gate pull requests, see pytest
* [ ] Test installed wheel in CI
* [ ] Use properly GitHub Packages, Releases, and Deployments
* [ ] Avoid having to pass `tmp_dir` to tests calling `assert_roundtrip_ok`
* [ ] `xarray` integration

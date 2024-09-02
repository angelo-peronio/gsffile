# Development notes of `gsffile`

## How to release

Push a tag named `v[major].[minor].[patch]`.

## Roadmap

* [ ] [pre-commit](https://learn.scientific-python.org/development/guides/style/)
    * [ ] mypy?
    * [ ] ci
    * [ ] shield
* [ ] ci
    * [ ] Test workflow to gate pull requests / branch protection, see pytest
    * [ ] Test installed wheel in CI
    * [ ] Use properly GitHub Packages, Releases, and Deployments
* [ ] `xarray` integration
* [ ] Release script
* [ ] Avoid having to pass `tmp_dir` to tests calling `assert_roundtrip_ok`

# Development notes of `gsffile`

## How to release

Push a tag named `v[major].[minor].[patch]`. Do not "synchronize changes", GitHub actions does not seem to understand that. Instead:

* push the last commit,
* tag it,
* push the tag.

## Roadmap

* [ ] Conda recipe, shield
* [ ] Avoid having to pass `tmp_dir` to tests calling `assert_roundtrip_ok`
* [ ] `xarray` integration
* [ ] pre-commit.ci, shield
* [ ] Test workflow to gate pull requests

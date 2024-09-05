# Development notes of `gsffile`

## How to release

Use `scripts\Release-Package.ps1`:

```powershell
.\scripts\Release-Package.ps1 -Version 1.2.3
```

## Roadmap

* [ ] [repo-review](https://learn.scientific-python.org/development/guides/repo-review/?repo=angelo-peronio%2Fgsffile&branch=master)
* [ ] [pre-commit](https://learn.scientific-python.org/development/guides/style/)
    * [ ] ci
    * [ ] shield
* [ ] ci
    * [ ] Test workflow to gate pull requests / branch protection, see pytest
    * [ ] Test installed wheel in CI
* [ ] `xarray` integration
* [ ] Avoid having to pass `tmp_dir` to tests calling `assert_roundtrip_ok`

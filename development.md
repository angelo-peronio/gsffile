# Development notes of `gsffile`

## How to release

Use `scripts\Release-Package.ps1`:

```powershell
.\scripts\Release-Package.ps1 -Version 1.2.3
```

## Roadmap

* [ ] [repo-review](https://learn.scientific-python.org/development/guides/repo-review/?repo=angelo-peronio%2Fgsffile&branch=master)
* [ ] ci
    * [ ] Test workflow to gate pull requests / [branch protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets), see [pytest](https://github.com/pytest-dev/pytest/tree/main/.github/workflows)
    * [ ] Test installed wheel in CI
    * [ ] Test against all supported NumPy versions
* [ ] `xarray` integration
* [ ] Logging
* [ ] Avoid having to pass `tmp_dir` to tests calling `assert_roundtrip_ok`

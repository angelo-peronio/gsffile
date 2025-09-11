# Development notes of `gsffile`

## How to release

Use `scripts\Release-Project.ps1`:

```powershell
.\scripts\Release-Project.ps1 -Bump patch
```

## Possibilities

* [ ] Test workflow to gate pull requests / [branch protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets), see [pytest](https://github.com/pytest-dev/pytest/tree/main/.github/workflows)
* [ ] `xarray` integration
* [ ] Avoid having to pass `tmp_dir` to tests calling `assert_roundtrip_ok`
* [ ] [Parallelize](https://nox.thea.codes/en/stable/cookbook.html#generating-a-matrix-with-github-actions) `nox` test sessions in GitHub Actions.

## Notes

* [repo-review](https://learn.scientific-python.org/development/guides/repo-review/?repo=angelo-peronio%2Fgsffile&branch=master)

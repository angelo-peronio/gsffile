# Development notes of `gsffile`

## How to release

Use `scripts\Release-Package.ps1`:

```powershell
.\scripts\Release-Package.ps1 -Version 1.2.3
```

## Roadmap

* [ ] Document logging in readme
* [ ] Fix codecov upload
* [ ] ci
    * [ ] Test workflow to gate pull requests / [branch protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets), see [pytest](https://github.com/pytest-dev/pytest/tree/main/.github/workflows)
    * [ ] Test installed wheel in CI
* [ ] `xarray` integration
* [ ] Avoid having to pass `tmp_dir` to tests calling `assert_roundtrip_ok`

## Ideas

* [repo-review](https://learn.scientific-python.org/development/guides/repo-review/?repo=angelo-peronio%2Fgsffile&branch=master)
* <https://hynek.me/articles/ditch-codecov-python>
* <https://hynek.me/articles/python-github-actions/>
* <https://cjolowicz.github.io/posts/hypermodern-python-06-ci-cd/#coverage-reporting-with-codecov>

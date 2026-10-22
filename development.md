# Development notes of `gsffile`

## How to release

Use `scripts\Release-Project.ps1`:

```powershell
.\scripts\Release-Project.ps1 -Bump patch
```

The script updates the changelog and citation, commits, tags, and pushes.
Pushing a version tag triggers the release workflow; it does not publish to
TestPyPI.

## CI workflows

| Workflow | Triggers | Publishing after successful checks |
| --- | --- | --- |
| `.github\workflows\ci.yaml` | Branch pushes, PRs to master, and manual runs | TestPyPI only on `master` |
| `.github\workflows\check.yaml` | Called by CI and release workflows | None; builds and inspects the package, audits dependencies, tests, and uploads coverage |
| `.github\workflows\release.yaml` | Version-tag pushes matching `v[0-9]+.[0-9]+.[0-9]+` | PyPI, then a GitHub Release |

Both entry workflows call `check.yaml` from the same commit and explicitly pass
`CODECOV_TOKEN`. Publishing jobs download the `Packages` artifact produced by
their own run. A master push and its release tag still run checks separately,
but only the master CI run can publish to TestPyPI.

Releases remain tag-triggered; there is no manual release button. Prefer
**Re-run failed jobs** when retrying an existing release. Repeating successful
uploads can fail on duplicate versions; partial uploads or an already-created
GitHub Release may require manual recovery. Manual CI runs on `master` still
publish to TestPyPI, whereas manual CI runs against tags only run checks.

## Possibilities

* [ ] Test workflow to gate pull requests / [branch protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets), see [pytest](https://github.com/pytest-dev/pytest/tree/main/.github/workflows)
* [ ] `xarray` integration
* [ ] Avoid having to pass `tmp_dir` to tests calling `assert_roundtrip_ok`
* [ ] [Parallelize](https://nox.thea.codes/en/stable/cookbook.html#generating-a-matrix-with-github-actions) `nox` test sessions in GitHub Actions.

## Notes

* [repo-review](https://learn.scientific-python.org/development/guides/repo-review/?repo=angelo-peronio%2Fgsffile&branch=master)

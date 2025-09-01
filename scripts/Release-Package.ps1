#Requires -Version 7.4
<#
    .SYNOPSIS
    Bump version, tag a release and push to origin.

    .DESCRIPTION
    Bump the project version, tag a release and push to remotes/origin.
    A CI pipeline will then build, test, and release.

    .EXAMPLE
    PS> .\scripts\Release-Package.ps1 -Bump patch

    .NOTES
    Requires [bump-my-version](https://github.com/callowayproject/bump-my-version)
#>

Param (
    [Parameter(Mandatory, HelpMessage = "What version component to bump.")]
    [ValidateSet("major", "minor", "patch")]
    [string]$VersionComponent
)

$PSNativeCommandUseErrorActionPreference = $true
$ErrorActionPreference = "Stop"

git fetch --all --tags

$CurrentBranch = git branch --show-current
if ($CurrentBranch -ne "master") {
    throw "Release invoked, but not on master branch.`n" `
        + "You probably want to merge your work into master. Quitting."
}

# https://stackoverflow.com/a/50737015
# https://stackoverflow.com/questions/3258243/check-if-pull-needed-in-git/17192101#comment23385634_3258271
$UpToDate = git rev-list HEAD..origin/master --count
if (-Not $UpToDate) {
    throw "Local repository is not up-to-date. Run git pull. Quitting."
}

$ProjectRootFolder = (Get-Item $PSScriptRoot).Parent.FullName
$ProjectName = Split-Path $ProjectRootFolder -Leaf
&"C:\venvs\$ProjectName\Scripts\activate.ps1"
bump-my-version bump $VersionComponent --verbose
deactivate

git push --follow-tags

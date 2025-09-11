<#
    .SYNOPSIS
    Bump version, tag a release and push to origin.

    .DESCRIPTION
    Bump the project version, tag a release, and push to remotes/origin.
    A CI pipeline will then build, test, and release.

    .EXAMPLE
    PS> .\scripts\Release-Project.ps1 -Bump patch

    .NOTES
    Requires bump-my-version <https://github.com/callowayproject/bump-my-version>.
#>

Param (
    # What version component to bump, either "major", "minor", or "patch".
    [Parameter(Mandatory, HelpMessage = "What version component to bump.")]
    [ValidateSet("major", "minor", "patch")]
    [string]$Bump,
    [switch]$DryRun
)

#Requires -Version 7.4
$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $true
Import-Module -Name "$PSScriptRoot\Utils.psm1"

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

$DryRunOption = ($DryRun) ? "--dry-run" : $null
uv run $(Get-UvRunOptions) bump-my-version bump $Bump $DryRunOption --verbose

if (-not ($DryRun)) {
    git push --follow-tags
}

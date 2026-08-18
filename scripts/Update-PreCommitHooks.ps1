<#
    .SYNOPSIS
    Update pre-commit hooks.
#>

#Requires -Version 7.4
$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $true
Import-Module -Name "$PSScriptRoot\Utils.psm1"

# As of 2026-03-06, the latest release tag of cffconvert is 2.0.0.
# It does not include the pre-commit hook, causing `pre-commit autoupdate` to fail.
# https://github.com/citation-file-format/cffconvert/issues/389#issuecomment-2480672136
uv run $(Get-UvRunOptions) prek autoupdate --exclude-repo="https://github.com/citation-file-format/cffconvert" --jobs=4

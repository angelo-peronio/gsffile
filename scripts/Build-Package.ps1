<#
    .SYNOPSIS
    Build source distribution and wheel, then expand them for inspection.

    .NOTES
    Requires uv <https://docs.astral.sh/uv/>.
#>

#Requires -Version 7.4
$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $true
Import-Module -Name "$PSScriptRoot\Utils.psm1"

Get-ProjectRootFolder | Push-Location
# Remove previous build artifacts.
if (Test-Path dist) { Remove-Item -Recurse -Force dist }
# Build
uv build
# Expand sdist and wheel.
Push-Location dist
Get-Item *.tar.gz | ForEach-Object { tar -xvzf $_ }
Get-Item *.whl | Expand-Archive -Verbose
Pop-Location
Pop-Location

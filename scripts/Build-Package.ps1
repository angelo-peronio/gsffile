#Requires -Version 7.4
<#
    .SYNOPSIS
    Build source distribution and wheel, then expand them for inspection.

    .NOTES
    Requires uv <https://docs.astral.sh/uv/>.
#>

$PSNativeCommandUseErrorActionPreference = $true
$ErrorActionPreference = "Stop"

$ProjectRootFolder = (Get-Item $PSScriptRoot).Parent.FullName

Push-Location $ProjectRootFolder
if (Test-Path dist) { Remove-Item -Recurse -Force dist }
uv build
Push-Location dist
Get-Item *.tar.gz | ForEach-Object { tar -xvzf $_ }
Get-Item *.whl | Expand-Archive -Verbose
Pop-Location
Pop-Location

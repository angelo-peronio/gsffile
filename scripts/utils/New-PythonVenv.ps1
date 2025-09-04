#Requires -Version 7.4
<#
    .SYNOPSIS
    Create or refresh a Python virtual enviroment.

    .DESCRIPTION
    Usage:
        * copy into your project,
        * set the default values of the parameters at your convenience,
        * execute.
    This script requires a `pyproject.toml`, and
        * if present, installs the corresponding package in editable mode
        * if present, installs the "dev" dependency group,
    The virtual enviroment is replaced if it already exists.
    The pinned versions specified e.g. in `uv.lock` or `pylock.toml` are ignored.
    Placing the environment outside the project folder avoids synchronization issues
    with Microsoft OneDrive.
    Requires uv <https://docs.astral.sh/uv/>.

    .EXAMPLE
    PS> .\scripts\New-PythonVenv.ps1

    .EXAMPLE
    PS> .\New-PythonVenv.ps1 -OutsideProjectFolder
#>

param (
    # Place the environemnt environemnt outside the project folder, in $VenvsRootFolder
    [switch]$OutsideProjectFolder = $false,
    # Folder containing the enviroments created with -OutsideProjectFolder
    [string]$VenvsRootFolder = "C:\venvs",
    # Python version to use. If feasible, specify it in pyproject.toml or .python-version, instead.
    # Defaults to the latest installed version.
    [string]$PythonVersion = "",
    # Location of the project root folder relative to the folder containing this script.
    # Common values are "." or "..".
    [string]$ProjectRoot = "../.."
)

$PSNativeCommandUseErrorActionPreference = $true
$ErrorActionPreference = "Stop"

$ProjectRoot = Join-Path $PSScriptRoot $ProjectRoot | Resolve-Path
"Project root folder: $ProjectRoot" | Write-Host
$ProjectName = Split-Path $ProjectRoot -Leaf
if ($OutsideProjectFolder) {
    $Env:UV_PROJECT_ENVIRONMENT = Join-Path $VenvsRootFolder $ProjectName
}

Push-Location $ProjectRoot
try {
    uv sync --upgrade
}
finally {
    Pop-Location
}

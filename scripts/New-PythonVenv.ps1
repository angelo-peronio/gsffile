#Requires -Version 7
<#
    .SYNOPSIS
    Create a Python virtual enviroment.

    .DESCRIPTION
    Usage: copy into either
        * the project root folder, or
        * an immediate subfolder named `scripts`
    and execute.
    If a `pyproject.toml` is found, also installs the corresponding package
    in editable mode, including its "dev" optional dependencies.
    If a `requirements.txt` is found, also installs the packages listed therein.
    The virtual enviroment can be placed outside the project folder, in a global location,
    to avoid synchronization issues with Microsoft OneDrive.
    The virtual enviroment is replaced if it already exists.
    Requires uv <https://docs.astral.sh/uv/>.

    .EXAMPLE
    PS> .\scripts\New-PythonVenv.ps1

    .EXAMPLE
    PS> .\New-PythonVenv.ps1 -OutsideProjectFolder
#>

param (
    # Place the environemnt environemnt outside the project folder, in a global location.
    [switch]$OutsideProjectFolder = $true,
    # Python version to use. If feasible, specify it in pyproject.toml or .python-version, instead.
    # Defaults to the latest installed version.
    [string]$PythonVersion = ""
)
$ErrorActionPreference = "Stop"
$VenvsRootFolder = "C:\venvs"

$InsideScriptsFolder = (Get-Item $PSScriptRoot).Name.ToLowerInvariant().Equals("scripts")
$ProjectRoot = ($InsideScriptsFolder) ? (Get-Item $PSScriptRoot).Parent : $PSScriptRoot
$ProjectName = Split-Path $ProjectRoot -Leaf
$VenvFolder = ($OutsideProjectFolder) ? (Join-Path $VenvsRootFolder $ProjectName) : ".venv"

Push-Location $ProjectRoot

uv venv --python=$PythonVersion $VenvFolder --prompt=$ProjectName

if (Test-Path -Path pyproject.toml -PathType Leaf) {
    "Found pyproject.toml. Installing..." | Write-Host
    uv pip install --python=$VenvFolder --editable .[dev]
}
if (Test-Path -Path requirements.txt -PathType Leaf) {
    "Found requirements.txt. Installing..." | Write-Host
    uv pip install --python=$VenvFolder --requirement requirements.txt
}

Pop-Location

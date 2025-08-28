#Requires -Version 7.4
<#
    .SYNOPSIS
    Create a Python virtual enviroment.

    .DESCRIPTION
    Usage:
        * copy into your project,
        * set the default values of the parameters at your convenience,
        * execute.
    If a `pyproject.toml` is found, also installs the corresponding package
    in editable mode, including its "dev" optional dependencies.
    If a `requirements.txt` is found, also installs the packages listed therein.
    The virtual enviroment is replaced if it already exists.
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
    [switch]$OutsideProjectFolder = $true,
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
$VenvFolder = $OutsideProjectFolder ? (Join-Path $VenvsRootFolder $ProjectName) : ".venv"

Push-Location $ProjectRoot
try {
    uv venv --python=$PythonVersion --prompt=$ProjectName --clear $VenvFolder

    if (Test-Path -Path pyproject.toml -PathType Leaf) {
        "Found pyproject.toml. Installing..." | Write-Host
        uv pip install --python=$VenvFolder --group=dev --editable=.
    }
    if (Test-Path -Path requirements.txt -PathType Leaf) {
        "Found requirements.txt. Installing..." | Write-Host
        uv pip install --python=$VenvFolder --requirement requirements.txt
    }
}
finally {
    Pop-Location
}

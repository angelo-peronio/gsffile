<#
    .SYNOPSIS
    Create a Python virtual enviroment in a global location.

    .DESCRIPTION
    Usage: copy into either
        * the project root folder, or
        * an immediate subfolder named `scripts`
    and execute.
    If a `pyproject.toml` is found, also installs the corresponding package
    in editable mode, including its "dev" optional dependencies.
    If a `requirements.txt` is found, also installs the packages listed therein.
    The virtual enviroment is placed outside the project folder to avoid synchronization
    issues with Microsoft OneDrive.
    The virtual enviroment is replaced if it already exists.
    Requires uv <https://docs.astral.sh/uv/>.

    .EXAMPLE
    PS> .\New-PythonVenv.ps1

    .EXAMPLE
    PS> .\scripts\New-PythonVenv.ps1
#>

$ErrorActionPreference = 'Stop'
$VenvsRootFolder = "C:\venvs"
# If feasible, constrain the Python version in pyproject.toml, instead.
# Empty string for latest installed version.
$PythonVersion = ""

if ($PSScriptRoot
    | Split-Path -Leaf
    | ForEach-Object ToLower
    | ForEach-Object Equals("scripts")) {
    # This script is in /scripts
    $ProjectRootFolder = (Get-Item $PSScriptRoot).Parent
}
else {
    # This script is in the project root
    $ProjectRootFolder = $PSScriptRoot
}

$ProjectName = Split-Path $ProjectRootFolder -Leaf
$VenvFolder = Join-Path $VenvsRootFolder $ProjectName

uv venv --python=$PythonVersion $VenvFolder

Push-Location $ProjectRootFolder
if (Test-Path -Path pyproject.toml -PathType Leaf) {
    "Found pyproject.toml. Installing..." | Write-Host
    uv pip install --python=$VenvFolder --editable .[dev]
}
if (Test-Path -Path requirements.txt -PathType Leaf) {
    "Found requirements.txt. Installing..." | Write-Host
    uv pip install --python=$VenvFolder --requirement requirements.txt
}
Pop-Location

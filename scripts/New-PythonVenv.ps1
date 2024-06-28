# Create a Python virtual enviroment in a global location,
# possibly replacing an existing one.
# Usage: copy into either
#   * the project root folder, or
#   * an immediate subfolder named `scripts`
# and exectute.
# Having the virtual enviroment outside the project folder prevents OneDrive sync issues.
# If a pyproject.toml is present, install the corresponding package in editable mode.
# If a requirements.txt is present, install the packages listed therein.

$ErrorActionPreference = 'Stop'

$PythonVersion = ""  # Empty string for latest installed version.
$VenvsRootFolder = "C:\venvs"

if ($Env:VIRTUAL_ENV) { 
    "Active virtual environment detected. Please deactivate it "
    "before trying again. Quitting." | Write-Host
    Exit 1
}

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
New-Item $VenvFolder -ItemType Directory -Force | Out-Null

"Using $(py -V:$PythonVersion --version) " `
    + "at $(py -V:$PythonVersion -c "import sys; print(sys.executable)")" | Write-Host
"Recreating Python virtual environment in $VenvFolder" | Write-Host
py -V:$PythonVersion -m venv $VenvFolder --clear --upgrade-deps
&"$VenvFolder\Scripts\Activate.ps1"
# First install wheel, to be able to wheel-install setup.py-only packages.
python -m pip install wheel

Push-Location $ProjectRootFolder
if (Test-Path -Path pyproject.toml -PathType Leaf) {
    "Found pyproject.toml. Installing..." | Write-Host
    python -m pip install --editable .[dev]
}
if (Test-Path -Path requirements.txt -PathType Leaf) {
    "Found requirements.txt. Installing..." | Write-Host
    python -m pip install --requirement requirements.txt
}
Pop-Location

deactivate

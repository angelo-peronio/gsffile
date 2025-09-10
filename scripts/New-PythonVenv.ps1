<#
    .SYNOPSIS
    Create or refresh a Python virtual environment.

    .DESCRIPTION
    This script requires a `pyproject.toml` configuration file, and
        * if present, installs the corresponding package in editable mode
        * if present, installs the "dev" dependency group,
    The virtual enviroment is replaced if it already exists.
    The pinned versions specified e.g. in `uv.lock` or `pylock.toml` are ignored.
    Requires uv <https://docs.astral.sh/uv/>.

    .EXAMPLE
    PS> .\scripts\New-PythonVenv.ps1
#>

#Requires -Version 7.4
$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $true
Import-Module -Name "$PSScriptRoot\Utils.psm1"

"Project root folder: $(Get-ProjectRootFolder)" | Write-Host

# As of uv 0.8.15, `uv sync` does not support an `--env-file` option like `uv run` does,
# so we run `uv sync` through `uv run`.
# Trick from https://github.com/astral-sh/uv/issues/8862#issuecomment-2474164670
uv run $(Get-UvRunOptions) uv sync --upgrade

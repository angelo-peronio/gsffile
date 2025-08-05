#Requires -Version 7.4
<#
    .SYNOPSIS
    Bootstrap a development environment.
#>

$PSNativeCommandUseErrorActionPreference = $true
$ErrorActionPreference = "Stop"

&"$PSScriptRoot\New-PythonVenv.ps1"

C:\Venvs\gsffile\Scripts\activate.ps1
pre-commit install --install-hooks --overwrite
deactivate

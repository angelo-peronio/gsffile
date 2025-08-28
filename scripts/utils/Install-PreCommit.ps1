#Requires -Version 7.4
<#
    .SYNOPSIS
    Install pre-commit.
#>

$PSNativeCommandUseErrorActionPreference = $true
$ErrorActionPreference = "Stop"

$ProjectRootFolder = (Get-Item $PSScriptRoot).Parent.Parent.FullName
$ProjectName = Split-Path $ProjectRootFolder -Leaf

&"C:\venvs\$ProjectName\Scripts\activate.ps1"
pre-commit install --install-hooks --overwrite
deactivate

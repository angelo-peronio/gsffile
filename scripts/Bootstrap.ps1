#Requires -Version 7.4
<#
    .SYNOPSIS
    Bootstrap a development environment.
#>

$PSNativeCommandUseErrorActionPreference = $true
$ErrorActionPreference = "Stop"

&"$PSScriptRoot\utils\New-PythonVenv.ps1"
&"$PSScriptRoot\utils\Install-PreCommit.ps1"

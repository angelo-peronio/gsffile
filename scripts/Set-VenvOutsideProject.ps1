<#
    .SYNOPSIS
    Tell `uv` to store the Python virtual environment outside the project folder.

    .DESCRIPTION
    Write an .env file inside the project root folder with an environment variable
    that tells `uv` to store the Python virtual environment under the $VenvsRootFolder
    defined below.
    Placing the environment outside the project folder avoids synchronization issues
    with Microsoft OneDrive, e.g. <https://github.com/astral-sh/uv/issues/7906>.
    Errors if the .env file already exists.

    .EXAMPLE
    PS> .\scripts\Set-VenvOutsideProject.ps1
#>

#Requires -Version 7.4
$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $true
Import-Module -Name "$PSScriptRoot\Utils.psm1"

$VenvsRootFolder = "C:\venvs"

$VenvFolder = Join-Path $VenvsRootFolder $(Get-ProjectName)
# `uv` accepts only forward slashes as path separator.
$Setting = "UV_PROJECT_ENVIRONMENT=$VenvFolder" -replace "\\", "/"
$EnvFilePath = Get-EnvFilePath

if (Test-Path $EnvFilePath -PathType Leaf) {
    throw "$EnvFilePath exists already. Edit it by hand to include $Setting. Quitting."
}
else {
    $Setting | Out-File $EnvFilePath
    "Written $EnvFilePath" | Write-Host
}

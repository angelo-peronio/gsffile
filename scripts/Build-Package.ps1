# Python packaging.
$ErrorActionPreference = "Stop"

$ProjectRootFolder = (Get-Item $PSScriptRoot).Parent.FullName
$ProjectName = Split-Path $ProjectRootFolder -Leaf
$Python = "C:\venvs\$ProjectName\Scripts\python.exe"

Push-Location $ProjectRootFolder
if (Test-Path dist) { Remove-Item -Recurse dist }
&$Python -m build
Push-Location dist
Get-Item *.tar.gz | ForEach-Object { tar -xvzf $_ }
Get-Item *.whl | Expand-Archive -Verbose
Pop-Location
Pop-Location
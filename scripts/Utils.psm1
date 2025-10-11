function Get-ProjectRootFolder {
    <#
        .SYNOPSIS
        Get the path of the root folder of the project

        .DESCRIPTION
        Looks for the first parent folder containing a `pyproject.toml` file.

        .OUTPUTS
        A string with the path of the root folder of the project.
    #>

    $Folder = $PSScriptRoot
    while ($Folder -ne "") {
        $Folder = Split-Path $Folder -Parent
        $PyprojectPath = Join-Path $Folder "pyproject.toml"
        if (Test-Path $PyprojectPath -PathType Leaf) {
            return $Folder
        }
    }
    throw "Cannot determine the project root folder. " `
        + "`pyproject.toml` not found in any parent folder of $PSScriptRoot"
}


function Get-ProjectName {
    <#
        .SYNOPSIS
        Get the name of the project.

        .DESCRIPTION
        Get the name of the folder containing the project.

        .OUTPUTS
        A string with the name of the project.
    #>

    Get-ProjectRootFolder
    | Split-Path -Leaf
    | Write-Output
}


function Get-EnvFilePath {
    <#
        .SYNOPSIS
        Get the path to the `.env` file inside the project root folder.

        .OUTPUTS
        A string.
    #>

    Get-ProjectRootFolder
    | Join-Path -ChildPath ".env"
    | Write-Output
}


function Get-UvRunOptions {
    <#
        .SYNOPSIS
        Get the command line options we use to invoke `uv run`.

        .OUTPUTS
        An array of option strings.

        .EXAMPLE
        PS> uv run $(Get-UvRunOptions) ruff check
    #>

    $EnvFilePath = Get-EnvFilePath
    # uv implements custom escaping for the --env-file option, so
    # we need to use / as path separator, and escape the whitespaces with \
    # https://github.com/astral-sh/uv/issues/15806
    # https://github.com/astral-sh/uv/pull/15815
    $EnvFilePathEscaped = $EnvFilePath.Replace("\", "/").Replace(" ", "\ ")
    $EnvFileOption = (Test-Path $EnvFilePath -PathType Leaf) ? "--env-file=$EnvFilePathEscaped" : $null
    @(
        "--directory=$(Get-ProjectRootFolder)",
        $EnvFileOption,
        "--"
    ) | Write-Output
}

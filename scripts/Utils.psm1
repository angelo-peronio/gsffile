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


function Get-UvEnvFileOption {
    <#
        .SYNOPSIS
        Get the --env-file command line option for `uv run`.

        .OUTPUTS
        If an `.env` file is found inside the project root folder returns
        "--env-file=<path to the .env file>", otherwise returns nothing.
    #>

    $EnvFilePath = Get-EnvFilePath
    if (Test-Path $EnvFilePath -PathType Leaf) {
        "--env-file=$EnvFilePath" | Write-Output
    }
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

    @(
        "--directory=$(Get-ProjectRootFolder)",
        $(Get-UvEnvFileOption),
        "--"
    ) | Write-Output
}

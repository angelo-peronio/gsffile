set default-list := true
set shell := ["pwsh", "-NoLogo", "-NoProfileLoadTime", "-Command"]
set script-interpreter := ["pwsh", "-NoLogo", "-NoProfileLoadTime", "-Command"]

[group("bootstrap")]
bootstrap: venv hooks-install

[group("bootstrap")]
[script]
venv:
    uv sync
    $PythonVersion = uv run python --version
    $PythonPath = uv run python -c "import sys; print(sys.executable)"
    "$PythonVersion at $PythonPath" | Write-Host

[group("bootstrap")]
hooks-install:
    uv run prek install --install-hooks --overwrite

[group("upgrade")]
upgrade: python-upgrade hooks-upgrade

[group("upgrade")]
python-upgrade:
    uv python upgrade
    uv lock --upgrade

[group("upgrade")]
hooks-upgrade:
    uv run prek autoupdate --jobs=4

build:
    uv build --clear
    Get-Item dist\*.tar.gz | ForEach-Object { tar -xvzf $_  -C dist }
    Get-Item dist\*.whl | Expand-Archive -Verbose -DestinationPath dist

test:
    uv run pytest

nox *args:
    uv run nox {{args}}

hooks:
    uv run prek run --all-files

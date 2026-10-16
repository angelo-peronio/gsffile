set minimum-version := "1.55.0"
set default-list
set shell := ["pwsh", "-NoLogo", "-NoProfileLoadTime", "-Command"]
set script-interpreter := ["pwsh", "-NoLogo", "-NoProfileLoadTime", "-Command"]

# Bootstrap a development environment
[group("bootstrap")]
bootstrap: venv hooks-install

# Create a Python virtual environment from the lockfile
[group("bootstrap")]
[script]
venv:
    uv sync
    $PythonVersion = uv run python --version
    $PythonPath = uv run python -c "import sys; print(sys.executable)"
    "$PythonVersion at $PythonPath" | Write-Host

# Install git pre-commit hooks
[group("bootstrap")]
hooks-install:
    uv run prek install --install-hooks --overwrite

# Upgrade everything
[group("upgrade")]
upgrade: python-upgrade hooks-upgrade

# Upgrade Python runtime and dependencies
[group("upgrade")]
python-upgrade:
    uv python upgrade
    uv lock --upgrade

# Upgrade git pre-commit hooks
[group("upgrade")]
hooks-upgrade:
    uv run prek autoupdate --jobs=4

# Build the package
build:
    uv build --clear
    Get-Item dist\*.tar.gz | ForEach-Object { tar -xvzf $_  -C dist }
    Get-Item dist\*.whl | Expand-Archive -Verbose -DestinationPath dist

# Remove all untracked files and directories
clean:
    git clean --force -d -x

# Run tests
[group("test")]
test:
    uv run pytest

# Run tests under multiple Python versions
[group("test")]
nox *args:
    uv run nox {{ args }}

# Run pre-commit hooks on all files
hooks:
    uv run prek run --all-files

# Auto-format the justfile
fmt:
    uv run just --fmt

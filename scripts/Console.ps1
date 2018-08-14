# Launch a console for the project.

$project_root = Split-Path $PSScriptRoot

$venv = Join-Path $project_root "venv\scripts\Activate.ps1"
if (-Not (Test-Path $venv)) {
    . $PSScriptRoot\Setup.ps1
}

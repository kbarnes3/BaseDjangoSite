# Runs manage.py from a consistent context
param(
    [string[]] $Arguments
)

$project_root = Split-Path $PSScriptRoot
$already_activated = . $PSScriptRoot\Ensure-Venv.ps1

$python = Join-Path $project_root "venv"

if (-Not $already_activated) {
    deactivate
}

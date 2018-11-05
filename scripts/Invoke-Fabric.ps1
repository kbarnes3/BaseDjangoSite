# Runs Fabric from a consistent context
# Any arguments passed into this function are passed to fab
param(
)

$project_root = Split-Path $PSScriptRoot
$already_activated = . $PSScriptRoot\Ensure-Venv.ps1

$fabric = Join-Path $project_root "venv\Scripts\fab.exe"
$web_dir = Join-Path $project_root "web"

Push-Location $web_dir
& $fabric $args
Pop-Location

if (-Not $already_activated) {
    deactivate
}

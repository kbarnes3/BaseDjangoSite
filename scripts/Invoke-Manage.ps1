# Runs manage.py from a consistent context
# Any arguments passed into this function are passed to manage.py
param(
)

$project_root = Split-Path $PSScriptRoot
$already_activated = . $PSScriptRoot\Ensure-Venv.ps1

$python = Join-Path $project_root "venv\Scripts\python.exe"
$web_dir = Join-Path $project_root "web"

Push-Location $web_dir
& $python manage.py $args
Pop-Location

if (-Not $already_activated) {
    deactivate
}

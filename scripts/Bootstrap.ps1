# Resolve all dependencies that the project requires to run.

$project_root = Split-Path $PSScriptRoot
$already_activated = . $PSScriptRoot\Ensure-Venv.ps1

Write-Warning "Updating pip"
& python -m pip install --upgrade pip --quiet
Write-Warning "Updating requirements"
& pip install -r (Join-Path $project_root "requirements.txt") --quiet
Write-Warning "Updating dev-requirements"
& pip install -r (Join-Path $project_root "dev-requirements.txt") --quiet

if (-Not $already_activated) {
    deactivate
}

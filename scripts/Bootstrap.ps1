# Resolve all dependencies that the project requires to run.
param(
    [switch]$Verbose
)

. $PSScriptRoot\Write-Status.ps1

if ($Verbose) {
    $quiet = ""
}
else {
    $quiet = "--quiet"
}

$project_root = Split-Path $PSScriptRoot
$already_activated = . $PSScriptRoot\Ensure-Venv.ps1

Write-Status "Updating pip"
& python -m pip install --upgrade pip $quiet
Write-Status "Updating requirements"
& pip install -r (Join-Path $project_root "requirements.txt") $quiet
Write-Status "Updating dev-requirements"
& pip install -r (Join-Path $project_root "dev-requirements.txt") $quiet

if (-Not $already_activated) {
    deactivate
}

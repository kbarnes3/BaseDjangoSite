# Set up project for the first time after , or set it back to the initial first unused state.

$project_root = Split-Path $PSScriptRoot

if ($env:VIRTUAL_ENV) {
    deactivate
}

# Remove local state if it exists
$venv = Join-Path $project_root "venv"
if (Test-Path $venv) {
    Write-Warning "Removing $venv"
    Remove-Item -Recurse -Force -Path $venv
}

$local_db = Join-Path $project_root "web\newdjangosite.db"
if (Test-Path $local_db) {
    Write-Warning "Removing $local_db"
    Remove-Item -Path $local_db
}

Write-Warning "Creating venv in $venv"
& py -3.6 -m venv $venv

. $PSScriptRoot\Bootstrap.ps1 -Verbose

. $PSScriptRoot\Ensure-Venv.ps1 | Out-Null

Write-Warning "Creating local database"
$manage = Join-Path $project_root "web\manage.py"
& python $manage migrate

Write-Warning "Creating super user"
& python $manage createsuperuser

deactivate

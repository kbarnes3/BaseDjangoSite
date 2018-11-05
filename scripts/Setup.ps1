# Set up project for the first time after , or set it back to the initial first unused state.
param(
    [switch]$GitClean
)

. $PSScriptRoot\Write-Status.ps1
$project_root = Split-Path $PSScriptRoot

if ($env:VIRTUAL_ENV) {
    deactivate
}

if ($GitClean) {
    Write-Status "Running 'git clean -df'"
    & git clean -df
}

# Remove local state if it exists
$venv = Join-Path $project_root "venv"
if (Test-Path $venv) {
    Write-Status "Removing $venv"
    Remove-Item -Recurse -Force -Path $venv
}

$local_db = Join-Path $project_root "web\newdjangosite.db"
if (Test-Path $local_db) {
    Write-Status "Removing $local_db"
    Remove-Item -Path $local_db
}

. $PSScriptRoot\Bootstrap.ps1 -Verbose

. $PSScriptRoot\Ensure-Venv.ps1 | Out-Null

Write-Status "Creating local database"
& $PSScriptRoot\Invoke-Manage.ps1 migrate

Write-Status "Creating super user"
& $PSScriptRoot\Invoke-Manage.ps1 createsuperuser

deactivate

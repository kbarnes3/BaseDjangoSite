# This script updates the project to run for its current checkout.
param(
    [switch]$Verbose
)

. $PSScriptRoot\Write-Status.ps1
$already_activated = . $PSScriptRoot\Ensure-Venv.ps1

# Check Python version
$venv_version = & python --version
$installed_version = & py -3.6 --version
if ($venv_version -ne $installed_version) {
    Write-Status "Updating venv from $venv_version to $installed_version"
    deactivate
    $project_root = Split-Path $PSScriptRoot
    $venv = Join-Path $project_root "venv"
    & py -3.6 -m venv $venv --upgrade
    . $PSScriptRoot\Ensure-Venv.ps1 | Out-Null
}

. $PSScriptRoot\Bootstrap.ps1 -Verbose:$Verbose

Write-Status "Performing database migrations"
. $PSScriptRoot\Invoke-Manage.ps1 migrate

if (-Not $already_activated) {
    deactivate
}

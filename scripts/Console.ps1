# Launch a console for the project.
param(
    [switch]$Quick,
    [switch]$Verbose
)

$project_root = Split-Path $PSScriptRoot
. $PSScriptRoot\Write-Status.ps1

Write-Status "NewDjangoSite console"

$venv = Join-Path $project_root "venv\scripts\Activate.ps1"
if (Test-Path $venv) {
    if (-Not($Quick)) {
        . $PSScriptRoot\Update.ps1 -Verbose:$Verbose
    }
}
else {
    if ($Quick) {
        Write-Warning "No virtual env detected, -Quick will be ignored"
    }
    . $PSScriptRoot\Setup.ps1
}

. $PSScriptRoot\Ensure-Venv.ps1 | Out-Null

# Register helper functions
Set-Item function:global:Invoke-Manage {
    . $PSScriptRoot\Invoke-Manage.ps1 $args
} -Force

Set-Item function:global:Invoke-Fabric {
    . $PSScriptRoot\Invoke-Fabric.ps1 $args
} -Force

Set-Item function:global:Start-Server {
    Invoke-Manage runserver $args
} -Force

Write-Status "NewDjangoSite ready"

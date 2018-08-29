# Launch a console for the project.
param(
    [switch]$Verbose
)

$project_root = Split-Path $PSScriptRoot

$venv = Join-Path $project_root "venv\scripts\Activate.ps1"
if (Test-Path $venv) {
    . $PSScriptRoot\Update.ps1 -Verbose:$Verbose
}
else {
    . $PSScriptRoot\Setup.ps1
}

. $PSScriptRoot\Ensure-Venv.ps1 | Out-Null

if (-Not (Test-Path variable:global:WriteStatusDefined)) {

    function global:Write-Status()
    {
        Write-Host -ForegroundColor Yellow -BackgroundColor Black $args
    }

    $global:WriteStatusDefined = $true
}

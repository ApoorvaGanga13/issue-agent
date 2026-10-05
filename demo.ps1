Set-Location $PSScriptRoot
docker info 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Docker Desktop is not running. Start it, wait until it says it is running, then run this again."
    exit 1
}
$env:SANDBOX = "docker"
Start-Job { Start-Sleep -Seconds 3; Start-Process "http://127.0.0.1:8000" } | Out-Null
& .\.venv\Scripts\python.exe -m uvicorn app:app --port 8000

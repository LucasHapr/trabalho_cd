# Script PowerShell para executar o Dashboard V2

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Dashboard Fitness V2" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Ativar ambiente virtual
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "`nAtivando ambiente virtual..." -ForegroundColor Yellow
    & ".\venv\Scripts\Activate.ps1"
} else {
    Write-Host "`n[ERRO] Ambiente virtual nao encontrado!" -ForegroundColor Red
    Write-Host "Execute: python -m venv venv" -ForegroundColor Yellow
    exit 1
}

# Verificar dataset
if (-not (Test-Path "data\external\fitlife_clean.csv")) {
    Write-Host "`n[ERRO] Dataset nao encontrado!" -ForegroundColor Red
    Write-Host "Arquivo esperado: data\external\fitlife_clean.csv" -ForegroundColor Yellow
    exit 1
}

Write-Host "[OK] Dataset encontrado" -ForegroundColor Green

# Executar dashboard
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Iniciando Dashboard..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "`nURL: http://localhost:8501" -ForegroundColor Green
Write-Host "Pressione Ctrl+C para encerrar`n" -ForegroundColor Yellow

streamlit run app_v2.py

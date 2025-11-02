# Script PowerShell simplificado para executar o projeto

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Dashboard Streamlit - Ciencia de Dados" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Criar diretórios se não existirem
Write-Host "`nCriando diretorios necessarios..." -ForegroundColor Yellow
$directories = @(
    "data\external",
    "data\processed",
    "reports\figs_interactive",
    "reports\figs_static",
    "models"
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "  [OK] $dir" -ForegroundColor Green
    }
}

# Verificar se streamlit está instalado
Write-Host "`nVerificando Streamlit..." -ForegroundColor Yellow
$streamlitInstalled = python -c "import streamlit" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "  [AVISO] Streamlit nao encontrado!" -ForegroundColor Red
    Write-Host "  Execute: pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}
Write-Host "  [OK] Streamlit instalado" -ForegroundColor Green

# Executar aplicação
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Iniciando Dashboard..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "`nAguarde o navegador abrir automaticamente..." -ForegroundColor Yellow
Write-Host "URL: http://localhost:8501" -ForegroundColor Green
Write-Host "`nPressione Ctrl+C para encerrar" -ForegroundColor Yellow
Write-Host ""

streamlit run app.py

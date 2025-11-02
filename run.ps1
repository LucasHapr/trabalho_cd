# Script PowerShell para executar o projeto

# Criar diretórios se não existirem
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
        Write-Host "Criado diretorio: $dir" -ForegroundColor Green
    }
}

# Verificar se ambiente virtual existe
if (-not (Test-Path "venv")) {
    Write-Host "Ambiente virtual nao encontrado. Criando..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "Ambiente virtual criado" -ForegroundColor Green
}

# Ativar ambiente virtual
Write-Host "`nAtivando ambiente virtual..." -ForegroundColor Cyan
& ".\venv\Scripts\Activate.ps1"

# Verificar se dependências estão instaladas
Write-Host "`nVerificando dependencias..." -ForegroundColor Cyan
$pipList = pip list
if ($pipList -notmatch "streamlit") {
    Write-Host "Dependencias nao instaladas. Instalando..." -ForegroundColor Yellow
    pip install -r requirements.txt
    Write-Host "Dependencias instaladas" -ForegroundColor Green
} else {
    Write-Host "Dependencias ja instaladas" -ForegroundColor Green
}

# Executar aplicação
Write-Host "`nIniciando dashboard Streamlit..." -ForegroundColor Cyan
Write-Host "Aguarde o navegador abrir automaticamente..." -ForegroundColor Cyan
Write-Host "URL: http://localhost:8501" -ForegroundColor Green
streamlit run app.py

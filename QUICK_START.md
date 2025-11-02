# 🚀 Guia de Início Rápido

Este guia vai te ajudar a executar o projeto em **5 minutos**.

## ⚡ Quick Start

### Opção 1: Usar Script PowerShell (Recomendado para Windows)

```powershell
# Execute o script de inicialização
.\run.ps1
```

Este script automaticamente:
- ✅ Cria os diretórios necessários
- ✅ Cria ambiente virtual (se não existir)
- ✅ Instala dependências
- ✅ Inicia o dashboard

### Opção 2: Passo a Passo Manual

```powershell
# 1. Criar ambiente virtual
python -m venv venv

# 2. Ativar ambiente
.\venv\Scripts\activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Gerar dados de exemplo (opcional)
python generate_sample_data.py

# 5. Executar dashboard
streamlit run app.py
```

## 📂 Preparar Seus Dados

### Dataset Wearable (JSON) - Já Incluído

O arquivo `data/runs_simulated.json` já está no projeto. Se quiser usar seus próprios dados:

```json
[
  {
    "id": "R001",
    "data": "2024-01-15",
    "idade": 28,
    "genero": "M",
    "altura_cm": 175,
    "peso_kg": 70,
    "distancia_km": 5.2,
    "duracao_min": 32,
    "calorias_kcal": 380,
    "bpm_medio": 145,
    "passos": 6800,
    "condicao_saude": "Bom",
    "nivel_fumante": "Não Fumante"
  }
]
```

### Dataset Público (CSV) - Opcional

Se você tem um dataset público (ex: FitLife do Kaggle):

1. Coloque o arquivo em `data/external/fitlife.csv`
2. Ative no dashboard ou em `conf/config.yaml`:

```yaml
use_public: true
use_wearable: true
```

**Ou gere dados de exemplo**:

```powershell
python generate_sample_data.py
```

## 🎮 Usando o Dashboard

Após executar `streamlit run app.py`, o navegador abrirá automaticamente.

### Sidebar (Esquerda)

1. **Selecionar Datasets**: Marque qual dataset usar
2. **Filtros**: Escolha faixas de idade, status de fumante, período, etc.

### Abas Principais

- **🚬 Fumantes vs Não Fumantes**: Compare performance em esportes
- **🏃 Runners vs Não Runners**: Análise de pace e métricas
- **📅 Prática por Idade**: Como varia a atividade física por idade
- **💓 BPM Praticantes**: Comparação de BPM entre grupos

### KPIs no Topo

- Total de registros
- BPM médio
- Pace médio
- % Fumantes
- % Praticantes

## 📊 Executar Pipeline Completo (Batch)

Para processar tudo de uma vez e gerar relatórios:

```powershell
python run_pipeline.py
```

Isso irá:
1. ✅ Carregar e processar dados
2. ✅ Executar todas as 4 análises
3. ✅ Gerar visualizações (HTML + PNG)
4. ✅ Treinar modelos preditivos
5. ✅ Salvar tudo em `reports/`

## 🔧 Troubleshooting Rápido

### "No module named 'streamlit'"

```powershell
pip install -r requirements.txt
```

### "FileNotFoundError: data/runs_simulated.json"

O arquivo já deve existir. Se não:

```powershell
python generate_sample_data.py
```

### "Nenhum dataset foi carregado"

No dashboard, marque pelo menos uma opção na sidebar:
- ☑️ Usar Dataset Wearable (JSON)

### Dashboard não abre automaticamente

Acesse manualmente: http://localhost:8501

### Erro de permissão no PowerShell

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 📁 Estrutura de Arquivos Importante

```
trabalho_cd/
├── app.py                    # 👈 Dashboard principal
├── run_pipeline.py           # 👈 Pipeline batch
├── generate_sample_data.py   # 👈 Gerar dados de exemplo
├── conf/
│   ├── config.yaml           # ⚙️ Configuração geral
│   └── data.yaml             # ⚙️ Caminhos dos dados
├── data/
│   └── runs_simulated.json   # 📊 Dados wearable
└── src/
    ├── preprocess.py         # 🔧 Processamento
    ├── analysis.py           # 📈 Análises
    └── plots.py              # 🎨 Visualizações
```

## 🎯 Próximos Passos

1. ✅ Execute o dashboard: `streamlit run app.py`
2. ✅ Explore as 4 análises nas abas
3. ✅ Teste os filtros na sidebar
4. ✅ Adicione seu próprio dataset público (opcional)
5. ✅ Execute o pipeline completo: `python run_pipeline.py`

## 💡 Dicas

- **Filtros dinâmicos**: Use a sidebar para focar em grupos específicos
- **Export de gráficos**: Passe o mouse sobre os gráficos e clique no ícone da câmera
- **Dados processados**: Ficam salvos em `data/processed/` (formato Parquet)
- **Visualizações**: Salvas em `reports/figs_interactive/` (HTML) e `reports/figs_static/` (PNG)

## 📚 Documentação Completa

Para mais detalhes, consulte o [README.md](README.md) principal.

---

**🎉 Pronto! Agora é só explorar o dashboard!**

Dúvidas? Verifique o README.md completo ou os docstrings no código.

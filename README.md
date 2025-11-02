# 🏃 Projeto de Ciência de Dados - Análise de Fitness e Saúde

Projeto completo de Ciência de Dados que analisa dados de fitness e saúde, comparando métricas entre diferentes grupos (fumantes, praticantes de corrida, faixas etárias) com visualizações interativas e modelos preditivos.

## 📋 Sumário

- [Visão Geral](#visão-geral)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)
- [Análises Implementadas](#análises-implementadas)
- [Tecnologias](#tecnologias)
- [Desenvolvimento](#desenvolvimento)

## 🎯 Visão Geral

Este projeto implementa um pipeline completo de Ciência de Dados que:

- ✅ Carrega e processa datasets de fitness (público + wearable)
- ✅ Valida dados com schemas Pandera
- ✅ Cria features derivadas (pace, cadência, IMC, etc.)
- ✅ Executa 4 análises estatísticas principais
- ✅ Gera visualizações interativas (Plotly) e estáticas (Seaborn/Matplotlib)
- ✅ Treina modelos preditivos (LightGBM) para BPM e Calorias
- ✅ Apresenta dashboard interativo com Streamlit

## 📁 Estrutura do Projeto

```
trabalho_cd/
├── conf/                          # Configurações Hydra
│   ├── config.yaml                # Configuração principal
│   └── data.yaml                  # Caminhos dos dados
├── data/
│   ├── external/                  # Dataset público (CSV/Parquet)
│   ├── runs_simulated.json        # Dataset wearable (JSON)
│   └── processed/                 # Dados processados (Parquet)
├── src/
│   ├── __init__.py
│   ├── dataio.py                  # I/O (CSV, Parquet, JSON)
│   ├── schema.py                  # Schemas de validação Pandera
│   ├── preprocess.py              # Limpeza e feature engineering
│   ├── utils.py                   # Funções auxiliares
│   ├── analysis.py                # 4 análises principais
│   ├── plots.py                   # Visualizações
│   └── modeling.py                # Modelos LightGBM
├── reports/
│   ├── figs_interactive/          # Gráficos HTML (Plotly)
│   └── figs_static/               # Gráficos PNG (Seaborn)
├── models/                        # Modelos treinados
├── app.py                         # Dashboard Streamlit
├── pyproject.toml                 # Dependências e config
├── requirements.txt               # Dependências alternativas
└── README.md                      # Este arquivo
```

## 🚀 Instalação

### Pré-requisitos

- Python 3.9+
- pip ou poetry

### Instalação com pip

```powershell
# Clone o repositório (se aplicável)
# cd trabalho_cd

# Crie um ambiente virtual
python -m venv venv
.\venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt
```

### Instalação com poetry

```powershell
poetry install
poetry shell
```

## ⚙️ Configuração

### 1. Configurar Caminhos dos Dados

Edite `conf/data.yaml`:

```yaml
external:
  path: "data/external/fitlife.csv"  # Caminho do dataset público
  format: "csv"

wearable:
  path: "data/runs_simulated.json"   # Caminho do JSON de corridas
```

### 2. Ajustar Parâmetros

Edite `conf/config.yaml`:

```yaml
# Flags de uso
use_public: true
use_wearable: true

# Filtros
filters:
  idade_min: 0
  idade_max: 120
  data_inicio: null
  data_fim: null

# Faixas de idade
age_bins:
  bins: [0, 17, 24, 34, 44, 54, 64, 120]
  labels: ["<=17", "18-24", "25-34", "35-44", "45-54", "55-64", "65+"]
```

### 3. Estrutura do Dataset Público (Exemplo FitLife)

O dataset público deve conter as seguintes colunas (em PT ou EN):

- **PT**: ID, Data, Idade, Gênero, Altura, Peso, Duração, Calorias Queimadas, BPM, Passos, Condição de Saúde, Nível de Fumante, Tipo de Atividade
- **EN**: ID, Date, Age, Gender, Height, Weight, Duration, Calories Burned, BPM, Steps, Health Condition, Smoker Level, Activity Type

### 4. Estrutura do JSON Wearable

O JSON deve ser uma lista de objetos:

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

## 🎮 Uso

### Executar Dashboard Streamlit

```powershell
streamlit run app.py
```

O dashboard abrirá em `http://localhost:8501` com:

- **Sidebar**: Seleção de datasets e filtros
- **KPIs**: Métricas principais no topo
- **4 Abas**: Uma para cada análise

### Executar Pipeline de Preprocessamento (CLI)

```powershell
python -m src.preprocess
```

### Gerar Visualizações em Batch

```python
from hydra import compose, initialize
from src.dataio import load_data
from src.preprocess import preprocess_pipeline
from src.analysis import run_all_analyses
from src.plots import generate_all_plots

# Inicializar Hydra
with initialize(config_path="conf", version_base=None):
    cfg = compose(config_name="config")

# Carregar e processar dados
df_public = load_data(cfg.data.external.path)
df_wearable = load_data(cfg.data.wearable.path)
df_processed = preprocess_pipeline(df_public, df_wearable, cfg)

# Executar análises
results = run_all_analyses(df_processed, cfg.sport_activities)

# Gerar visualizações
generate_all_plots(df_processed, results, output_dir="reports")
```

### Treinar Modelos Preditivos

```python
from src.modeling import train_and_evaluate_models

# Treinar modelos para BPM e Calorias
models = train_and_evaluate_models(
    df_processed, 
    targets=["bpm", "calorias_kcal"],
    save_dir="models"
)
```

## 📊 Análises Implementadas

### 1. 🚬 Fumantes vs Não Fumantes em Esportes

**Objetivo**: Comparar performance em atividades esportivas entre fumantes e não fumantes.

**Métricas**:
- Pace (min/km)
- BPM médio
- Calorias queimadas
- Passos

**Visualizações**:
- Boxplot (pace)
- Barras com erro (BPM e calorias)

**Teste**: Mann-Whitney U test

---

### 2. 🏃 Praticantes vs Não Praticantes de Corrida

**Objetivo**: Comparar ritmo (pace) e outras métricas entre runners e não runners.

**Métricas**:
- Pace (min/km)
- Distância percorrida
- Duração
- BPM

**Visualizações**:
- Violin plot (distribuição de pace)
- ECDF (função de distribuição acumulada)
- Histograma com KDE

**Teste**: Mann-Whitney U test

---

### 3. 📅 Prática de Esportes por Faixas de Idade

**Objetivo**: Analisar como a prática varia entre idades.

**Métricas**:
- Taxa de praticantes (%)
- Duração média
- Distância média
- Calorias médias

**Visualizações**:
- Barras (taxa de praticantes)
- Barras empilhadas (praticantes vs não praticantes)
- Gráficos de métricas médias

---

### 4. 💓 BPM Praticantes vs Não Praticantes

**Objetivo**: Comparar BPM entre quem pratica e quem não pratica atividades.

**Métricas**:
- BPM médio geral
- BPM por faixa de idade
- BPM estratificado

**Visualizações**:
- Barras com erro (BPM médio)
- Heatmap (BPM por idade e status)
- Barras agrupadas

**Teste**: Mann-Whitney U test

## 🛠️ Tecnologias

### Core
- **Python 3.9+**
- **Pandas 2.0+**: Manipulação de dados
- **NumPy 1.24+**: Operações numéricas

### Data Validation & Storage
- **Pandera 0.17+**: Validação de schemas
- **PyArrow 12.0+**: Armazenamento Parquet

### Visualization
- **Plotly 5.17+**: Gráficos interativos
- **Seaborn 0.13+**: Gráficos estatísticos
- **Matplotlib 3.7+**: Gráficos estáticos

### Machine Learning
- **LightGBM 4.0+**: Gradient boosting
- **scikit-learn 1.3+**: Preprocessing e métricas
- **sktime 0.24+**: Séries temporais (opcional)

### App & Config
- **Streamlit 1.28+**: Dashboard interativo
- **Hydra-core 1.3+**: Gerenciamento de configurações

## 📈 Modelagem Preditiva (Bônus)

O projeto inclui modelos LightGBM para prever:

1. **BPM**: Predição de batimentos cardíacos
2. **Calorias**: Estimativa de calorias queimadas

**Features utilizadas**:
- Numéricas: idade, altura, peso, duração, distância, passos, IMC, pace, cadência
- Categóricas (one-hot): gênero, faixa de idade, condição de saúde, nível fumante, atividade
- Booleanas: is_runner, is_practitioner, is_smoker

**Métricas de avaliação**:
- MAE (Mean Absolute Error)
- RMSE (Root Mean Squared Error)
- R² (Coefficient of Determination)

**Exemplo de uso**:

```python
from src.modeling import train_and_evaluate_models, get_feature_importance_df

# Treinar
results = train_and_evaluate_models(df_processed)

# Ver importância das features
importance_df = get_feature_importance_df(results, target="bpm", top_n=10)
print(importance_df)
```

## 🧪 Desenvolvimento

### Executar Testes

```powershell
pytest tests/ -v --cov=src
```

### Formatação de Código

```powershell
# Black
black src/ app.py

# Ruff
ruff check src/ app.py
```

### Type Checking

```powershell
mypy src/
```

## 📝 Features Derivadas

O pipeline cria automaticamente as seguintes features:

| Feature | Descrição | Fórmula |
|---------|-----------|---------|
| `pace_min_km` | Ritmo em min/km | `duracao_min / distancia_km` |
| `cadencia_passos_min` | Cadência em passos/min | `passos / duracao_min` |
| `imc` | Índice de Massa Corporal | `peso_kg / (altura_m)²` |
| `is_runner` | Pratica corrida? | Baseado em `atividade` |
| `is_smoker` | É fumante? | Baseado em `nivel_fumante` |
| `is_practitioner` | Pratica esporte? | Regras combinadas |
| `faixa_idade` | Faixa etária | Binning de `idade` |

## 🔍 Validação de Dados

O projeto usa **Pandera** para validar:

✅ **Tipos**: Conversão automática com coerção  
✅ **Faixas**: BPM ∈ [30, 220], idade ∈ [5, 120], etc.  
✅ **Unicidade**: Por (id, dt)  
✅ **Coerência**: Pace vs distância/duração  

Linhas inválidas são **removidas** e **logadas**.

## 🎨 Personalização

### Adicionar Nova Análise

1. Crie função em `src/analysis.py`:

```python
def analyze_my_custom_analysis(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
    # Sua lógica aqui
    return df_summary, stats_dict
```

2. Adicione visualização em `src/plots.py`:

```python
def plot_my_custom_plot(df: pd.DataFrame) -> go.Figure:
    fig = px.scatter(df, x="x", y="y")
    return fig
```

3. Adicione aba no `app.py`:

```python
with tab5:
    st.header("Minha Análise")
    df_summary, stats = analyze_my_custom_analysis(df_filtered)
    fig = plot_my_custom_plot(df_filtered)
    st.plotly_chart(fig)
```

## 📦 Exportação de Resultados

### Salvar Dados Processados

```python
from src.dataio import save_parquet

save_parquet(df_processed, "data/processed/combined_data.parquet")
```

### Exportar Visualizações

Os gráficos são automaticamente salvos em:

- **Interativos**: `reports/figs_interactive/*.html`
- **Estáticos**: `reports/figs_static/*.png`

### Exportar Tabelas de Análise

```python
results["smokers_vs_nonsmokers"]["summary"].to_csv("reports/smokers_summary.csv")
```

## 🐛 Troubleshooting

### Erro: "FileNotFoundError: Arquivo não encontrado"

✅ Verifique os caminhos em `conf/data.yaml`  
✅ Certifique-se que os arquivos existem nas pastas corretas

### Erro: "Nenhum dataset foi processado"

✅ Ative `use_public` e/ou `use_wearable` em `conf/config.yaml`  
✅ Verifique se os arquivos são válidos (CSV/JSON)

### Erro de validação Pandera

✅ Revise o schema em `src/schema.py`  
✅ Linhas inválidas são automaticamente removidas (veja logs)

### Gráficos não aparecem no Streamlit

✅ Certifique-se que `plotly` está instalado  
✅ Verifique se há dados suficientes após filtros

## 📚 Referências

- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Plotly Python](https://plotly.com/python/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [LightGBM Documentation](https://lightgbm.readthedocs.io/)
- [Pandera Documentation](https://pandera.readthedocs.io/)
- [Hydra Documentation](https://hydra.cc/docs/intro/)

## 📄 Licença

Este projeto é fornecido como material educacional.

## 👤 Autor

Lucas - Trabalho de Ciência de Dados

---

**🎉 Projeto Completo e Funcional!**

Para executar: `streamlit run app.py`

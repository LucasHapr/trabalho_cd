# 🏃 Dashboard de Análise de Fitness e Saúde - V2

## 📊 Versão Otimizada para fitlife_clean.csv

Dashboard completo de análise de dados de fitness e saúde com 4 análises estatísticas, visualizações interativas e modo batch.

---

## 🎯 4 Análises Implementadas

### 1. 📊 Fumantes vs Não Fumantes
- **Objetivo**: Comparar métricas de saúde entre fumantes e não fumantes
- **Métricas**: BPM médio, Calorias queimadas
- **Testes**: Mann-Whitney U test
- **Visualizações**: Boxplots, Violin plots

### 2. 🏃 Praticantes de Corrida vs Não Praticantes  
- **Objetivo**: Comparar desempenho entre corredores e não corredores
- **Métricas**: BPM médio, Calorias queimadas
- **Testes**: Mann-Whitney U, Kolmogorov-Smirnov
- **Visualizações**: Boxplots, Histogramas sobrepostos

### 3. 👥 Prática de Esportes por Faixas de Idade
- **Objetivo**: Analisar taxa de praticantes e métricas por idade
- **Métricas**: Taxa de praticantes (%), BPM médio, Calorias médias
- **Testes**: Teste Chi-quadrado
- **Visualizações**: Gráficos de barras, Stacked bars

### 4. 💓 BPM Praticantes vs Não Praticantes
- **Objetivo**: Comparar BPM entre praticantes e não praticantes
- **Métricas**: BPM médio global e segmentado por idade
- **Testes**: T-test, Mann-Whitney U, Cohen's d (tamanho do efeito)
- **Visualizações**: Gráficos de barras, Heatmaps

---

## 🚀 Quick Start

### 1. Executar Dashboard Interativo

```powershell
# Ativar ambiente virtual
.\venv\Scripts\Activate.ps1

# Executar dashboard
streamlit run app_v2.py
```

Abra o navegador em: **http://localhost:8501**

### 2. Executar Análises em Batch Mode

```powershell
# Gerar todas as análises e salvar CSVs
python -m src.analysis_v2

# Gerar todos os gráficos (HTML + PNG)
python -m src.plots_v2
```

---

## 📁 Estrutura de Arquivos

```
trabalho_cd/
├── src/
│   ├── analysis_v2.py     # 4 funções de análise estatística
│   └── plots_v2.py         # Visualizações Plotly + Seaborn
│
├── data/
│   └── external/
│       └── fitlife_clean.csv    # Dataset principal (687,701 linhas)
│
├── reports/
│   ├── analysis_results/         # CSVs com resultados das análises
│   ├── figs_interactive/         # Gráficos HTML interativos (10 arquivos)
│   └── figs_static/              # Gráficos PNG estáticos (4 arquivos)
│
├── app_v2.py              # Dashboard Streamlit
└── README_V2.md           # Este arquivo
```

---

## 📊 Dataset: fitlife_clean.csv

### Informações
- **Total de linhas**: 687,701
- **Período**: 2024-01-01 a 2024-12-31
- **Faixas de idade**: 18-24, 25-34, 35-44, 45-54, 55-64

### Colunas Disponíveis

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `id` | int | ID do usuário |
| `dt` | datetime | Data do registro |
| `idade` | int | Idade do usuário |
| `genero` | str | Gênero (M/F) |
| `altura_cm` | float | Altura em cm |
| `peso_kg` | float | Peso em kg |
| `bpm` | int | Batimentos por minuto |
| `calorias_kcal` | float | Calorias queimadas |
| `atividade` | str | Tipo de atividade física |
| `condicao_saude` | str | Condição de saúde |
| `nivel_fumante` | str | Nível de fumante |
| `is_runner` | bool | É corredor? |
| `is_smoker` | bool | É fumante? |
| `is_practitioner` | bool | É praticante de atividade física? |
| `faixa_idade` | str | Faixa etária |

### Estatísticas
- **Fumantes**: 106,331 (15.5%)
- **Corredores**: 67,145 (9.8%)
- **Praticantes**: 342,402 (49.8%)
- **BPM médio**: 131.5
- **Calorias médias**: 15.4 kcal

---

## 🎨 Dashboard Features

### Filtros Disponíveis (Sidebar)
- ✅ **Faixas de Idade**: Seleção múltipla
- ✅ **Fumante**: Todos / Apenas Fumantes / Apenas Não Fumantes
- ✅ **Período**: Seletor de data (início e fim)

### KPIs no Topo
- Total de Registros
- Taxa de Fumantes (%)
- Taxa de Corredores (%)
- Taxa de Praticantes (%)
- BPM Médio

### 4 Abas de Análise
Cada aba contém:
- Tabelas com resultados agregados
- Testes estatísticos
- Visualizações interativas (Plotly)
- Possibilidade de zoom, hover e export

---

## 📈 Visualizações Geradas

### Interativas (HTML) - 10 arquivos

**Análise 1: Fumantes**
- `analise1_bpm_boxplot.html` - Boxplot de BPM
- `analise1_bpm_violin.html` - Violin plot de BPM
- `analise1_calorias_boxplot.html` - Boxplot de calorias

**Análise 2: Runners**
- `analise2_bpm_boxplot.html` - Boxplot de BPM
- `analise2_calorias_boxplot.html` - Boxplot de calorias
- `analise2_calorias_hist.html` - Histograma de calorias

**Análise 3: Faixa de Idade**
- `analise3_taxa_barras.html` - Taxa de praticantes
- `analise3_stacked.html` - Distribuição empilhada

**Análise 4: BPM**
- `analise4_comparacao.html` - Comparação global
- `analise4_heatmap.html` - Heatmap por idade

### Estáticas (PNG) - 4 arquivos
- `analise1_comparacao.png` - Fumantes: BPM e Calorias
- `analise2_comparacao.png` - Runners: BPM e Calorias
- `analise3_idade.png` - Prática por idade
- `analise4_bpm.png` - BPM praticantes vs não praticantes

---

## 🧪 Testes Estatísticos

### Mann-Whitney U Test
- Teste não-paramétrico para comparar duas amostras independentes
- Usado em: Análise 1, 2 e 4
- Significância: p < 0.05

### Teste Chi-quadrado
- Testa independência entre variáveis categóricas
- Usado em: Análise 3
- Significância: p < 0.05

### T-test
- Teste paramétrico para comparar médias
- Usado em: Análise 4
- Significância: p < 0.05

### Kolmogorov-Smirnov Test
- Compara distribuições completas
- Usado em: Análise 2
- Significância: p < 0.05

### Cohen's d
- Mede o tamanho do efeito
- Usado em: Análise 4
- Interpretação: small (< 0.5), medium (0.5-0.8), large (> 0.8)

---

## 📝 Uso das Funções

### Análises

```python
from src.analysis_v2 import (
    analyze_smokers_vs_nonsmokers,
    analyze_runners_vs_nonrunners,
    analyze_practice_by_age,
    analyze_bpm_practitioners_vs_nonpractitioners
)
import pandas as pd

# Carregar dados
df = pd.read_csv('data/external/fitlife_clean.csv')

# Análise 1
df_summary, stats = analyze_smokers_vs_nonsmokers(df)
print(df_summary)
print(stats)

# Análise 2
df_summary, stats = analyze_runners_vs_nonrunners(df)

# Análise 3
df_summary, stats = analyze_practice_by_age(df)

# Análise 4
df_global, df_by_age, stats = analyze_bpm_practitioners_vs_nonpractitioners(df)
```

### Visualizações

```python
from src.plots_v2 import (
    plot_smokers_comparison_boxplot,
    plot_runners_comparison_histogram,
    plot_practice_by_age_bars,
    plot_bpm_by_age_heatmap
)
from pathlib import Path

# Gerar gráfico interativo
fig = plot_smokers_comparison_boxplot(df, 'bpm')
fig.show()  # Exibir

# Ou salvar como HTML
fig = plot_smokers_comparison_boxplot(
    df, 
    'bpm', 
    save_path=Path('meu_grafico.html')
)
```

---

## 🔧 Dependências

```
pandas >= 2.0.0
numpy >= 1.24.0
scipy >= 1.10.0
plotly >= 5.17.0
seaborn >= 0.13.0
matplotlib >= 3.7.0
streamlit >= 1.28.0
```

Instalar todas:
```powershell
pip install -r requirements.txt
```

---

## 💡 Tips & Tricks

### 1. Filtrar dados específicos

```python
# Apenas fumantes entre 25-34 anos
df_filtered = df[
    (df['is_smoker'] == True) & 
    (df['faixa_idade'] == '25-34')
]

# Executar análise
df_summary, stats = analyze_smokers_vs_nonsmokers(df_filtered)
```

### 2. Exportar resultados

```python
# Salvar resultados em CSV
df_summary.to_csv('resultados_analise1.csv', index=False)

# Salvar gráfico como PNG
import plotly.io as pio
fig = plot_smokers_comparison_boxplot(df, 'bpm')
pio.write_image(fig, 'grafico.png', width=1200, height=600)
```

### 3. Comparar períodos

```python
# Primeiro semestre
df_h1 = df[df['dt'] < '2024-07-01']
summary_h1, _ = analyze_practice_by_age(df_h1)

# Segundo semestre
df_h2 = df[df['dt'] >= '2024-07-01']
summary_h2, _ = analyze_practice_by_age(df_h2)

# Comparar
import pandas as pd
comparison = pd.merge(
    summary_h1[['faixa_idade', 'taxa_praticantes_pct']], 
    summary_h2[['faixa_idade', 'taxa_praticantes_pct']], 
    on='faixa_idade',
    suffixes=('_h1', '_h2')
)
```

---

## 📚 Type Hints e Docstrings

Todas as funções seguem padrões Python com:
- ✅ Type hints completos
- ✅ Docstrings detalhadas (Google style)
- ✅ Tratamento de erros
- ✅ Validação de dados

Exemplo:

```python
def analyze_smokers_vs_nonsmokers(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
    """
    Análise 1: Fumantes vs Não Fumantes.
    
    Compara médias e medianas de bpm e calorias_kcal
    entre fumantes (is_smoker=True) e não fumantes (is_smoker=False).
    
    Args:
        df: DataFrame com colunas [is_smoker, bpm, calorias_kcal]
    
    Returns:
        Tuple contendo:
        - DataFrame com métricas agregadas por grupo
        - Dict com testes estatísticos
    """
    ...
```

---

## ✅ Checklist de Validação

- [x] 4 análises estatísticas implementadas e testadas
- [x] Funções com type hints e docstrings
- [x] Testes estatísticos (Mann-Whitney, Chi-quadrado, T-test, KS)
- [x] 10 gráficos interativos (HTML) gerados
- [x] 4 gráficos estáticos (PNG) gerados
- [x] Dashboard Streamlit com 4 tabs funcionando
- [x] Filtros na sidebar (idade, fumante, período)
- [x] KPIs exibidos no topo
- [x] Modo batch funcional (`python -m src.analysis_v2`)
- [x] Modo batch para gráficos (`python -m src.plots_v2`)
- [x] Dataset com 687k+ linhas processado

---

## 🎓 Resultados Principais

### Análise 1: Fumantes vs Não Fumantes
- **BPM**: Diferença significativa (p = 0.0146)
- **Calorias**: Sem diferença significativa (p = 0.5653)
- **Conclusão**: Fumantes têm BPM ligeiramente diferente, mas gasto calórico similar

### Análise 2: Runners vs Não Runners
- **BPM**: Sem diferença significativa (p = 0.5479)
- **Calorias**: Diferença altamente significativa (p < 0.0001)
- **Conclusão**: Corredores queimam significativamente mais calorias

### Análise 3: Prática por Faixa de Idade
- **Taxa global**: 49.8% são praticantes
- **Chi-quadrado**: p < 0.0001 (taxa varia por idade)
- **Conclusão**: Prática de esportes é dependente da faixa etária

### Análise 4: BPM Praticantes vs Não Praticantes
- **T-test**: p = 0.5525 (não significativo)
- **Cohen's d**: 0.001 (efeito muito pequeno)
- **Conclusão**: BPM médio é praticamente igual entre grupos

---

## 📞 Suporte

Para questões ou problemas:
1. Verifique se o dataset está em `data/external/fitlife_clean.csv`
2. Confirme que todas as dependências estão instaladas
3. Execute os testes em modo batch primeiro

---

## 🎉 Projeto Completo!

**✅ Todas as funcionalidades implementadas e testadas!**

- Análises estatísticas robustas
- Visualizações interativas e estáticas
- Dashboard profissional
- Modo batch para automação
- Código com type hints e documentação completa

**Execute agora: `streamlit run app_v2.py`** 🚀

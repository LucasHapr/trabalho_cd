# 🎯 CHECKLIST DE VALIDAÇÃO DO PROJETO

Use este checklist para validar que tudo está funcionando corretamente.

## ✅ Estrutura de Arquivos

- [ ] `conf/config.yaml` existe
- [ ] `conf/data.yaml` existe
- [ ] `data/runs_simulated.json` existe
- [ ] `src/` contém todos os módulos (.py)
- [ ] `app.py` existe na raiz
- [ ] `requirements.txt` existe

## ✅ Instalação

```powershell
# Verificar Python
python --version  # Deve ser 3.9+

# Criar ambiente virtual
python -m venv venv
.\venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Verificar instalações críticas
python -c "import streamlit; print('✓ Streamlit:', streamlit.__version__)"
python -c "import pandas; print('✓ Pandas:', pandas.__version__)"
python -c "import plotly; print('✓ Plotly:', plotly.__version__)"
python -c "import hydra; print('✓ Hydra OK')"
```

## ✅ Configuração

- [ ] `conf/data.yaml` aponta para `data/runs_simulated.json`
- [ ] `conf/config.yaml` tem `use_wearable: true`
- [ ] Diretórios criados:
  - [ ] `data/external/`
  - [ ] `data/processed/`
  - [ ] `reports/figs_interactive/`
  - [ ] `reports/figs_static/`
  - [ ] `models/`

## ✅ Testes Básicos

### 1. Testar Importação dos Módulos

```powershell
python -c "from src import dataio, schema, utils, preprocess, analysis, plots, modeling; print('✓ Todos os módulos importados')"
```

### 2. Testar Leitura do JSON

```powershell
python -c "from src.dataio import load_data; df = load_data('data/runs_simulated.json'); print(f'✓ JSON carregado: {len(df)} linhas')"
```

### 3. Testar Preprocessamento

```powershell
python -c "from src.dataio import load_data; from src.preprocess import clean_wearable_dataset; from hydra import compose, initialize; from pathlib import Path; config_dir = Path('conf'); from hydra import initialize_config_dir; with initialize_config_dir(config_dir=str(config_dir.absolute()), version_base=None): cfg = compose(config_name='config'); df = load_data('data/runs_simulated.json'); df_clean = clean_wearable_dataset(df, cfg); print(f'✓ Preprocessamento OK: {len(df_clean)} linhas')"
```

### 4. Executar Dashboard

```powershell
streamlit run app.py
```

**Verificar**:
- [ ] Dashboard abre no navegador (http://localhost:8501)
- [ ] Sidebar aparece com opções
- [ ] Checkbox "Usar Dataset Wearable (JSON)" marcado
- [ ] KPIs aparecem no topo
- [ ] 4 abas estão visíveis
- [ ] Gráficos carregam sem erros

## ✅ Funcionalidades do Dashboard

### Tab 1: Fumantes vs Não Fumantes
- [ ] Tabela de resumo aparece
- [ ] Gráfico de boxplot (pace) carrega
- [ ] Gráfico de barras (BPM) carrega
- [ ] Testes estatísticos aparecem

### Tab 2: Runners vs Não Runners
- [ ] Tabela de resumo aparece
- [ ] Violin plot carrega
- [ ] ECDF carrega
- [ ] Testes estatísticos aparecem

### Tab 3: Prática por Idade
- [ ] Tabela de taxas aparece
- [ ] Gráfico de barras (taxa) carrega
- [ ] Gráfico empilhado carrega
- [ ] Tabela de métricas aparece

### Tab 4: BPM Praticantes
- [ ] Tabela de resumo aparece
- [ ] Gráfico de barras (BPM) carrega
- [ ] Heatmap carrega
- [ ] Teste estatístico aparece

### Filtros da Sidebar
- [ ] Filtro de faixa de idade funciona
- [ ] Filtro de status de fumante funciona
- [ ] Filtro de praticante funciona
- [ ] Filtro de período funciona
- [ ] Contador de registros atualiza

## ✅ Pipeline Completo

```powershell
python run_pipeline.py
```

**Verificar**:
- [ ] Pipeline executa sem erros
- [ ] Dados processados salvos em `data/processed/`
- [ ] Visualizações salvas em `reports/figs_interactive/`
- [ ] Visualizações salvas em `reports/figs_static/`
- [ ] Tabelas CSV salvas em `reports/`
- [ ] Modelos salvos em `models/` (se executado)

## ✅ Qualidade do Código

```powershell
# Formatar código
black src/ app.py

# Verificar linting
ruff check src/ app.py
```

## 🐛 Troubleshooting Comum

### Erro: "No module named 'X'"
**Solução**: `pip install X` ou `pip install -r requirements.txt`

### Erro: "FileNotFoundError"
**Solução**: Verifique caminhos em `conf/data.yaml` e se arquivos existem

### Erro: "Nenhum dataset foi carregado"
**Solução**: Marque "Usar Dataset Wearable" na sidebar do dashboard

### Dashboard não abre
**Solução**: Acesse manualmente http://localhost:8501

### Erro de Hydra
**Solução**: Certifique-se que `conf/` existe e contém `config.yaml` e `data.yaml`

### Gráficos não aparecem
**Solução**: 
1. Verifique se há dados após filtros
2. Limpe cache: Ctrl+Shift+R no navegador
3. Reinicie o Streamlit

## 📊 Métricas de Sucesso

Após validação completa, você deve ter:

- ✅ Dashboard funcionando em http://localhost:8501
- ✅ 4 análises rodando sem erros
- ✅ Visualizações interativas carregando
- ✅ Filtros funcionando
- ✅ KPIs calculados corretamente
- ✅ Dados processados salvos
- ✅ Relatórios gerados

## 🎉 Projeto Validado!

Se todos os itens estão marcados, seu projeto está **100% funcional**!

### Próximos Passos Opcionais:

1. **Adicionar dataset público**: Coloque CSV em `data/external/` e ative `use_public: true`
2. **Personalizar análises**: Edite `src/analysis.py`
3. **Adicionar visualizações**: Edite `src/plots.py`
4. **Treinar modelos**: Execute com modelagem ativada
5. **Deploy**: Considere Streamlit Cloud, Heroku, ou Docker

---

**Data de Validação**: _____________

**Validado por**: _____________

**Status**: [ ] ✅ Aprovado  [ ] ⚠️ Pendências  [ ] ❌ Requer correções

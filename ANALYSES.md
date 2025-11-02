# 📊 Documentação das Análises Estatísticas

Este documento detalha as 4 análises principais implementadas no projeto.

---

## 🚬 Análise 1: Fumantes vs Não Fumantes em Esportes

### Objetivo
Investigar se existe diferença significativa no desempenho esportivo entre fumantes e não fumantes.

### Hipótese
**H₀**: Não há diferença significativa no desempenho entre fumantes e não fumantes  
**H₁**: Existe diferença significativa no desempenho entre fumantes e não fumantes

### Metodologia

1. **Filtro de Dados**: Apenas atividades esportivas (Running, Walking, Cycling, Swimming, Jogging, Hiking)
2. **Classificação**: Baseada na coluna `nivel_fumante` → `is_smoker`
3. **Métricas Analisadas**:
   - Pace (min/km)
   - BPM médio
   - Calorias queimadas (kcal)
   - Passos

4. **Teste Estatístico**: Mann-Whitney U test (não paramétrico)
   - Escolhido por não assumir distribuição normal
   - Compara medianas entre grupos independentes
   - Nível de significância: α = 0.05

### Interpretação dos Resultados

- **p-value < 0.05**: Diferença estatisticamente significativa
- **p-value ≥ 0.05**: Não há evidência de diferença significativa

### Visualizações

1. **Boxplot de Pace**: Mostra distribuição e outliers
2. **Barras com Erro (BPM)**: Média ± desvio padrão

### Insights Esperados

- Fumantes podem ter BPM mais alto em repouso
- Não fumantes podem ter melhor performance (pace menor)
- Maior variabilidade em fumantes ocasionais

---

## 🏃 Análise 2: Praticantes vs Não Praticantes de Corrida

### Objetivo
Comparar o ritmo (pace) e outras métricas entre quem pratica corrida regularmente e quem não pratica.

### Hipótese
**H₀**: Não há diferença no pace entre runners e não runners  
**H₁**: Runners têm pace significativamente melhor (menor)

### Metodologia

1. **Classificação**: Baseada em `atividade` contendo "Running" ou "Jogging" → `is_runner`
2. **Métricas Analisadas**:
   - Pace (min/km) - **métrica principal**
   - BPM médio
   - Distância percorrida
   - Duração
   - Calorias queimadas

3. **Teste Estatístico**: Mann-Whitney U test
4. **Análise Adicional**: Distribuição acumulada (ECDF)

### Interpretação dos Resultados

- **Pace menor** = melhor performance (mais rápido)
- **ECDF**: Mostra probabilidade acumulada de pace
  - Curva à esquerda = pace melhor em média
  - Maior separação = maior diferença entre grupos

### Visualizações

1. **Violin Plot**: Distribuição completa com densidade
2. **ECDF**: Função de distribuição acumulada
3. **Histograma com KDE**: Sobreposição de distribuições

### Insights Esperados

- Runners têm pace consistentemente menor
- Maior variabilidade em não runners
- Runners podem ter BPM mais baixo para mesma intensidade (melhor condicionamento)

---

## 📅 Análise 3: Prática de Esportes por Faixas de Idade

### Objetivo
Investigar como a prática de atividades físicas varia entre diferentes faixas etárias.

### Questões de Pesquisa

1. Qual faixa etária tem maior taxa de praticantes?
2. Como variam as métricas de performance por idade?
3. Há declínio de atividade com a idade?

### Metodologia

1. **Faixas de Idade**:
   - ≤17 anos
   - 18-24 anos
   - 25-34 anos
   - 35-44 anos
   - 45-54 anos
   - 55-64 anos
   - 65+ anos

2. **Definição de Praticante** (`is_practitioner`):
   - Pratica atividade esportiva listada, **OU**
   - Possui ≥ 1000 passos, **OU**
   - Possui ≥ 20 minutos de atividade

3. **Métricas Calculadas**:
   - Taxa de praticantes (%)
   - Duração média (min)
   - Distância média (km)
   - Calorias médias (kcal)
   - BPM médio

4. **Análise**: Estatística descritiva por grupo

### Interpretação dos Resultados

- **Taxa > 50%**: Alta adesão à atividade física
- **Tendência decrescente**: Possível redução com idade
- **Métricas médias**: Indicam intensidade típica por faixa

### Visualizações

1. **Barras Simples**: Taxa de praticantes (%)
2. **Barras Empilhadas**: Distribuição absoluta
3. **Gráficos de Métricas**: Comparação multi-faixa

### Insights Esperados

- Pico de atividade em 25-34 anos
- Possível declínio após 55 anos
- Jovens podem ter maior intensidade mas menor constância

---

## 💓 Análise 4: BPM Praticantes vs Não Praticantes

### Objetivo
Comparar a frequência cardíaca entre quem pratica atividades físicas regularmente e quem não pratica.

### Hipótese
**H₀**: Não há diferença no BPM entre praticantes e não praticantes  
**H₁**: Praticantes têm BPM significativamente diferente

### Metodologia

1. **Classificação**: Baseada em `is_practitioner`
2. **Métrica**: BPM (batimentos por minuto)
3. **Análises**:
   - Comparação geral (todos os dados)
   - Estratificação por faixa etária
   - Heatmap de interação idade × status

4. **Teste Estatístico**: Mann-Whitney U test

### Interpretação dos Resultados

#### BPM em Repouso vs Atividade

- **Repouso**: 60-100 bpm (normal)
- **Atividade leve**: 100-120 bpm
- **Atividade moderada**: 120-150 bpm
- **Atividade intensa**: 150-180 bpm

#### Condicionamento Físico

- Praticantes podem ter:
  - **BPM em repouso mais baixo** (coração mais eficiente)
  - **BPM durante exercício relativamente mais alto** (maior capacidade)
  - **Recuperação mais rápida** (não medido aqui)

### Visualizações

1. **Barras com Erro**: BPM médio ± DP por grupo
2. **Heatmap**: BPM por (faixa_idade × status_praticante)
3. **Barras Agrupadas**: Comparação estratificada

### Insights Esperados

- Praticantes podem ter BPM mais regulado
- Diferença mais pronunciada em faixas etárias médias
- Menor variabilidade em praticantes regulares

---

## 🧪 Testes Estatísticos Utilizados

### Mann-Whitney U Test

**Quando usar**:
- Comparar dois grupos independentes
- Dados não seguem distribuição normal
- Variáveis ordinais ou contínuas

**Vantagens**:
- Não paramétrico (sem pressupostos de distribuição)
- Robusto a outliers
- Eficiente para amostras pequenas

**Interpretação**:
- **p-value < 0.001**: *** (altamente significativo)
- **p-value < 0.01**: ** (muito significativo)
- **p-value < 0.05**: * (significativo)
- **p-value ≥ 0.05**: ns (não significativo)

### Limitações

1. **Não mede magnitude**: Apenas indica se há diferença
2. **Não controla confounders**: Correlação ≠ causalidade
3. **Múltiplas comparações**: Considerar correção de Bonferroni se muitos testes

---

## 📈 Features Derivadas Utilizadas

### pace_min_km
```
pace = duracao_min / distancia_km
```
- Menor valor = melhor performance
- Típico para corrida: 5-7 min/km (amador)

### cadencia_passos_min
```
cadencia = passos / duracao_min
```
- Corrida: ~160-180 passos/min
- Caminhada: ~100-120 passos/min

### is_runner
```
is_runner = atividade.contains("Running|Jogging")
```

### is_smoker
```
is_smoker = nivel_fumante.contains("Fumante") 
           & ~nivel_fumante.contains("Não|Ex")
```

### is_practitioner
```
is_practitioner = (atividade in sport_activities)
                | (passos >= 1000)
                | (duracao_min >= 20)
```

### faixa_idade
```
faixa = pd.cut(idade, bins=[0,17,24,34,44,54,64,120])
```

---

## 🎯 Critérios de Qualidade

### Validação de Dados

- ✅ Valores dentro de faixas fisiológicas
- ✅ Consistência entre variáveis (pace vs distancia/duracao)
- ✅ Remoção de outliers extremos
- ✅ Tratamento de missings

### Tamanho Amostral

- **Mínimo recomendado**: 30 observações por grupo
- **Ideal**: 100+ observações por grupo
- **Alerta**: n < 10 (resultados inconclusivos)

### Significância Prática vs Estatística

- **Significância estatística**: p-value < 0.05
- **Significância prática**: Diferença relevante no contexto
  - Ex: 0.5 min/km em pace é praticamente significativo
  - Ex: 2 bpm de diferença pode não ser relevante

---

## 📚 Referências

### Valores de Referência

- **BPM**: American Heart Association
- **Pace**: Runner's World
- **OMS**: Recomendações de atividade física

### Metodologia Estatística

- Mann, H. B.; Whitney, D. R. (1947). "On a Test of Whether one of Two Random Variables is Stochastically Larger than the Other"
- Scipy Documentation: scipy.stats.mannwhitneyu

---

**Última Atualização**: Novembro 2025  
**Autor**: Lucas - Trabalho de Ciência de Dados

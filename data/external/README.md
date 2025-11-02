# Dataset Público - Exemplo de Estrutura

Este diretório deve conter o dataset público de fitness (ex: FitLife do Kaggle).

## Formato Esperado

### CSV com colunas em Português:
- ID
- Data
- Idade
- Gênero
- Altura
- Peso
- Duração
- Calorias Queimadas
- BPM
- Passos
- Condição de Saúde
- Nível de Fumante
- Tipo de Atividade

### Ou em Inglês:
- ID
- Date
- Age
- Gender
- Height
- Weight
- Duration
- Calories Burned
- BPM
- Steps
- Health Condition
- Smoker Level
- Activity Type

## Como Adicionar

1. Baixe o dataset FitLife ou similar
2. Coloque o arquivo neste diretório (ex: `fitlife.csv`)
3. Atualize o caminho em `conf/data.yaml`:

```yaml
external:
  path: "data/external/fitlife.csv"
  format: "csv"
```

## Formatos Suportados

- CSV (`.csv`)
- Parquet (`.parquet`)

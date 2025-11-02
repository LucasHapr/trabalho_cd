"""
Módulo de definição de schemas Pandera para validação de dados.

Este módulo define os schemas de validação para os datasets público e wearable,
garantindo integridade de tipos, faixas de valores e coerência dos dados.
"""

from typing import Optional

import pandas as pd
import pandera as pa
from pandera import Column, DataFrameSchema, Check


# Schema base com colunas comuns
BASE_SCHEMA = {
    "id": Column(
        pa.String,
        nullable=False,
        coerce=True,
        checks=[Check.str_length(min_value=1)],
        description="Identificador único da sessão",
    ),
    "dt": Column(
        pa.DateTime,
        nullable=False,
        coerce=True,
        description="Data e hora da sessão",
    ),
    "idade": Column(
        pa.Int,
        nullable=False,
        checks=[Check.in_range(min_value=5, max_value=120)],
        coerce=True,
        description="Idade do participante em anos",
    ),
    "genero": Column(
        pa.String,
        nullable=True,
        coerce=True,
        description="Gênero do participante",
    ),
    "altura_cm": Column(
        pa.Float,
        nullable=True,
        checks=[Check.in_range(min_value=120.0, max_value=230.0)],
        coerce=True,
        description="Altura em centímetros",
    ),
    "peso_kg": Column(
        pa.Float,
        nullable=True,
        checks=[Check.in_range(min_value=30.0, max_value=250.0)],
        coerce=True,
        description="Peso em kilogramas",
    ),
    "duracao_min": Column(
        pa.Float,
        nullable=True,
        checks=[Check.greater_than_or_equal_to(0.0)],
        coerce=True,
        description="Duração da atividade em minutos",
    ),
    "calorias_kcal": Column(
        pa.Float,
        nullable=True,
        checks=[Check.greater_than_or_equal_to(0.0)],
        coerce=True,
        description="Calorias queimadas em kcal",
    ),
    "bpm": Column(
        pa.Float,
        nullable=True,
        checks=[Check.in_range(min_value=30.0, max_value=220.0)],
        coerce=True,
        description="Batimentos cardíacos por minuto",
    ),
    "passos": Column(
        pa.Int,
        nullable=True,
        checks=[Check.greater_than_or_equal_to(0)],
        coerce=True,
        description="Número de passos",
    ),
    "condicao_saude": Column(
        pa.String,
        nullable=True,
        coerce=True,
        description="Condição de saúde do participante",
    ),
    "nivel_fumante": Column(
        pa.String,
        nullable=True,
        coerce=True,
        description="Nível de fumante",
    ),
}

# Schema para dataset público (inclui atividade, pode não ter distância)
PUBLIC_SCHEMA_DICT = {
    **BASE_SCHEMA,
    "atividade": Column(
        pa.String,
        nullable=True,
        coerce=True,
        description="Tipo de atividade física",
    ),
    "distancia_km": Column(
        pa.Float,
        nullable=True,
        checks=[Check.greater_than_or_equal_to(0.0)],
        coerce=True,
        description="Distância percorrida em km",
    ),
}

# Schema para dataset wearable (corrida, sempre tem distância)
WEARABLE_SCHEMA_DICT = {
    **BASE_SCHEMA,
    "distancia_km": Column(
        pa.Float,
        nullable=False,
        checks=[Check.greater_than(0.0)],
        coerce=True,
        description="Distância percorrida em km",
    ),
    "atividade": Column(
        pa.String,
        nullable=True,
        coerce=True,
        default="Running",
        description="Tipo de atividade (default: Running)",
    ),
}

# Criação dos schemas
public_schema = DataFrameSchema(
    columns=PUBLIC_SCHEMA_DICT,
    strict=False,
    coerce=True,
    description="Schema para validação do dataset público FitLife",
)

wearable_schema = DataFrameSchema(
    columns=WEARABLE_SCHEMA_DICT,
    strict=False,
    coerce=True,
    description="Schema para validação do dataset wearable (JSON corridas)",
)

# Schema para dados processados (após feature engineering)
PROCESSED_SCHEMA_DICT = {
    **BASE_SCHEMA,
    "atividade": Column(pa.String, nullable=True, coerce=True),
    "distancia_km": Column(
        pa.Float,
        nullable=True,
        checks=[Check.greater_than_or_equal_to(0.0)],
        coerce=True,
    ),
    "pace_min_km": Column(
        pa.Float,
        nullable=True,
        checks=[Check.greater_than_or_equal_to(0.0)],
        coerce=True,
        description="Pace em minutos por km",
    ),
    "cadencia_passos_min": Column(
        pa.Float,
        nullable=True,
        checks=[Check.greater_than_or_equal_to(0.0)],
        coerce=True,
        description="Cadência em passos por minuto",
    ),
    "is_runner": Column(
        pa.Bool,
        nullable=True,
        coerce=True,
        description="Indica se pratica corrida",
    ),
    "is_practitioner": Column(
        pa.Bool,
        nullable=False,
        coerce=True,
        description="Indica se pratica alguma atividade física",
    ),
    "is_smoker": Column(
        pa.Bool,
        nullable=False,
        coerce=True,
        description="Indica se é fumante",
    ),
    "faixa_idade": Column(
        pa.Category,
        nullable=False,
        coerce=True,
        description="Faixa etária",
    ),
    "imc": Column(
        pa.Float,
        nullable=True,
        checks=[Check.in_range(min_value=10.0, max_value=60.0)],
        coerce=True,
        description="Índice de Massa Corporal",
    ),
}

processed_schema = DataFrameSchema(
    columns=PROCESSED_SCHEMA_DICT,
    strict=False,
    coerce=True,
    description="Schema para dados processados com features derivadas",
)


def validate_dataframe(
    df: pd.DataFrame, schema_type: str = "processed", lazy: bool = True
) -> tuple[pd.DataFrame, Optional[pd.DataFrame]]:
    """
    Valida um DataFrame usando o schema especificado.

    Args:
        df: DataFrame a ser validado
        schema_type: Tipo de schema ('public', 'wearable', 'processed')
        lazy: Se True, acumula todos os erros; se False, para no primeiro erro

    Returns:
        Tupla (df_valid, df_invalid) onde:
        - df_valid: DataFrame com linhas válidas
        - df_invalid: DataFrame com linhas inválidas (ou None se todas válidas)

    Raises:
        ValueError: Se schema_type não for reconhecido
    """
    schemas = {
        "public": public_schema,
        "wearable": wearable_schema,
        "processed": processed_schema,
    }

    if schema_type not in schemas:
        raise ValueError(
            f"schema_type deve ser um de {list(schemas.keys())}, recebido: {schema_type}"
        )

    schema = schemas[schema_type]

    try:
        # Tenta validar todo o DataFrame
        validated_df = schema.validate(df, lazy=lazy)
        return validated_df, None
    except pa.errors.SchemaErrors as err:
        # Se houver erros, separa linhas válidas de inválidas
        print(f"⚠️  Encontrados {len(err.failure_cases)} erros de validação:")
        print(err.failure_cases[["schema_context", "column", "check", "check_number"]])

        # Identifica índices com erros
        invalid_indices = err.failure_cases["index"].unique()
        valid_mask = ~df.index.isin(invalid_indices)

        df_valid = df[valid_mask].copy()
        df_invalid = df[~valid_mask].copy()

        print(f"✓ {len(df_valid)} linhas válidas, ✗ {len(df_invalid)} linhas inválidas removidas")

        return df_valid, df_invalid


def check_distance_coherence(
    df: pd.DataFrame, speed_col: str = "pace_min_km", tolerance: float = 0.1
) -> pd.DataFrame:
    """
    Verifica coerência entre distância, duração e velocidade.

    Args:
        df: DataFrame com colunas distancia_km, duracao_min e pace_min_km
        speed_col: Nome da coluna de velocidade
        tolerance: Tolerância percentual para discrepâncias (0.1 = 10%)

    Returns:
        DataFrame marcando linhas com discrepâncias
    """
    if not all(col in df.columns for col in ["distancia_km", "duracao_min", speed_col]):
        return df

    df = df.copy()

    # Calcula pace esperado
    mask = (df["distancia_km"] > 0) & (df["duracao_min"] > 0)
    df.loc[mask, "pace_expected"] = df.loc[mask, "duracao_min"] / df.loc[mask, "distancia_km"]

    # Verifica discrepâncias
    if "pace_expected" in df.columns:
        pace_diff = abs(df[speed_col] - df["pace_expected"]) / df["pace_expected"]
        df["pace_coherent"] = pace_diff <= tolerance

        incoherent_count = (~df["pace_coherent"]).sum()
        if incoherent_count > 0:
            print(f"⚠️  {incoherent_count} linhas com pace incoerente (>{tolerance*100}% diff)")

    return df


if __name__ == "__main__":
    # Teste básico dos schemas
    print("✓ Schemas definidos:")
    print(f"  - public_schema: {len(public_schema.columns)} colunas")
    print(f"  - wearable_schema: {len(wearable_schema.columns)} colunas")
    print(f"  - processed_schema: {len(processed_schema.columns)} colunas")

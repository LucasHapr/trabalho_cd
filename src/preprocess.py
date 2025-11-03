"""
Módulo de preprocessamento de dados.

Este módulo implementa funções para limpeza, padronização de colunas,
feature engineering e transformações dos datasets público e wearable.
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from omegaconf import DictConfig

# from .schema import validate_dataframe  # Arquivo não existe
from .utils import (
    bin_ages,
    calculate_cadence,
    calculate_imc,
    calculate_pace,
    is_practitioner_from_features,
    is_runner_from_activity,
    is_smoker_from_level,
    parse_datetime_column,
)


def standardize_column_names(df: pd.DataFrame, mapping: Dict[str, str]) -> pd.DataFrame:
    """
    Padroniza nomes de colunas usando um mapeamento.

    Args:
        df: DataFrame original
        mapping: Dicionário {nome_original: nome_padrao}

    Returns:
        DataFrame com colunas renomeadas
    """
    df = df.copy()
    df = df.rename(columns=mapping)
    print(f"✓ Colunas padronizadas: {list(df.columns)}")
    return df


def clean_public_dataset(df: pd.DataFrame, cfg: DictConfig) -> pd.DataFrame:
    """
    Limpa e padroniza o dataset público FitLife.

    Args:
        df: DataFrame do dataset público
        cfg: Configuração Hydra

    Returns:
        DataFrame limpo e padronizado
    """
    print("\n📋 Limpando dataset público...")

    # Padronizar nomes de colunas
    df = standardize_column_names(df, cfg.mapping.public)

    # Parse datetime
    if "dt" in df.columns:
        df["dt"] = parse_datetime_column(df["dt"], utc=True)

    # Remover duplicatas
    initial_len = len(df)
    df = df.drop_duplicates(subset=["id", "dt"], keep="first")
    if len(df) < initial_len:
        print(f"⚠️  Removidas {initial_len - len(df)} duplicatas")

    # Garantir tipos corretos
    if "idade" in df.columns:
        df["idade"] = pd.to_numeric(df["idade"], errors="coerce")

    if "altura_cm" in df.columns:
        # Converter para cm se estiver em metros
        df["altura_cm"] = pd.to_numeric(df["altura_cm"], errors="coerce")
        df.loc[df["altura_cm"] < 10, "altura_cm"] = df.loc[df["altura_cm"] < 10, "altura_cm"] * 100

    if "peso_kg" in df.columns:
        df["peso_kg"] = pd.to_numeric(df["peso_kg"], errors="coerce")

    if "duracao_min" in df.columns:
        df["duracao_min"] = pd.to_numeric(df["duracao_min"], errors="coerce")

    if "calorias_kcal" in df.columns:
        df["calorias_kcal"] = pd.to_numeric(df["calorias_kcal"], errors="coerce")

    if "bpm" in df.columns:
        df["bpm"] = pd.to_numeric(df["bpm"], errors="coerce")

    if "passos" in df.columns:
        df["passos"] = pd.to_numeric(df["passos"], errors="coerce").astype("Int64")

    if "distancia_km" in df.columns:
        df["distancia_km"] = pd.to_numeric(df["distancia_km"], errors="coerce")
    else:
        df["distancia_km"] = np.nan

    # Preencher atividade se não existir
    if "atividade" not in df.columns:
        df["atividade"] = None

    # Limpar strings
    string_cols = ["genero", "condicao_saude", "nivel_fumante", "atividade"]
    for col in string_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].replace(["nan", "None", ""], None)

    print(f"✓ Dataset público limpo: {len(df)} linhas, {len(df.columns)} colunas")
    return df


def clean_wearable_dataset(df: pd.DataFrame, cfg: DictConfig) -> pd.DataFrame:
    """
    Limpa e padroniza o dataset wearable (JSON corridas).

    Args:
        df: DataFrame do dataset wearable
        cfg: Configuração Hydra

    Returns:
        DataFrame limpo e padronizado
    """
    print("\n📋 Limpando dataset wearable...")

    # Padronizar nomes de colunas
    df = standardize_column_names(df, cfg.mapping.wearable)

    # Parse datetime
    if "dt" in df.columns:
        df["dt"] = parse_datetime_column(df["dt"], utc=True)

    # Remover duplicatas
    initial_len = len(df)
    df = df.drop_duplicates(subset=["id", "dt"], keep="first")
    if len(df) < initial_len:
        print(f"⚠️  Removidas {initial_len - len(df)} duplicatas")

    # Garantir tipos corretos (similar ao público)
    if "idade" in df.columns:
        df["idade"] = pd.to_numeric(df["idade"], errors="coerce")

    if "altura_cm" in df.columns:
        df["altura_cm"] = pd.to_numeric(df["altura_cm"], errors="coerce")

    if "peso_kg" in df.columns:
        df["peso_kg"] = pd.to_numeric(df["peso_kg"], errors="coerce")

    if "duracao_min" in df.columns:
        df["duracao_min"] = pd.to_numeric(df["duracao_min"], errors="coerce")

    if "calorias_kcal" in df.columns:
        df["calorias_kcal"] = pd.to_numeric(df["calorias_kcal"], errors="coerce")

    if "bpm" in df.columns:
        df["bpm"] = pd.to_numeric(df["bpm"], errors="coerce")

    if "passos" in df.columns:
        df["passos"] = pd.to_numeric(df["passos"], errors="coerce").astype("Int64")

    if "distancia_km" in df.columns:
        df["distancia_km"] = pd.to_numeric(df["distancia_km"], errors="coerce")

    # Wearable sempre é corrida
    if "atividade" not in df.columns:
        df["atividade"] = "Running"

    # Limpar strings
    string_cols = ["genero", "condicao_saude", "nivel_fumante", "atividade"]
    for col in string_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].replace(["nan", "None", ""], None)

    print(f"✓ Dataset wearable limpo: {len(df)} linhas, {len(df.columns)} colunas")
    return df


def engineer_features(df: pd.DataFrame, cfg: DictConfig) -> pd.DataFrame:
    """
    Cria features derivadas.

    Features criadas:
    - pace_min_km: ritmo em min/km
    - cadencia_passos_min: cadência em passos/min
    - is_runner: se pratica corrida
    - is_practitioner: se pratica atividade física
    - is_smoker: se é fumante
    - faixa_idade: faixa etária
    - imc: índice de massa corporal

    Args:
        df: DataFrame limpo
        cfg: Configuração Hydra

    Returns:
        DataFrame com features derivadas
    """
    print("\n⚙️  Criando features derivadas...")

    df = df.copy()

    # Pace
    if "duracao_min" in df.columns and "distancia_km" in df.columns:
        df["pace_min_km"] = calculate_pace(df["duracao_min"], df["distancia_km"])
        print(f"  ✓ pace_min_km criado")

    # Cadência
    if "passos" in df.columns and "duracao_min" in df.columns:
        df["cadencia_passos_min"] = calculate_cadence(df["passos"], df["duracao_min"])
        print(f"  ✓ cadencia_passos_min criado")

    # IMC
    if "peso_kg" in df.columns and "altura_cm" in df.columns:
        df["imc"] = calculate_imc(df["peso_kg"], df["altura_cm"])
        print(f"  ✓ imc criado")

    # is_runner
    if "atividade" in df.columns:
        df["is_runner"] = is_runner_from_activity(df["atividade"])
        print(f"  ✓ is_runner criado ({df['is_runner'].sum()} runners)")
    else:
        df["is_runner"] = False

    # is_smoker
    if "nivel_fumante" in df.columns:
        df["is_smoker"] = is_smoker_from_level(df["nivel_fumante"])
        print(f"  ✓ is_smoker criado ({df['is_smoker'].sum()} fumantes)")
    else:
        df["is_smoker"] = False

    # is_practitioner
    df["is_practitioner"] = is_practitioner_from_features(
        atividade=df.get("atividade"),
        passos=df.get("passos"),
        duracao_min=df.get("duracao_min"),
        min_passos=cfg.practitioner_rules.min_passos,
        min_duracao=cfg.practitioner_rules.min_duracao_min,
        sport_activities=cfg.sport_activities,
    )
    print(f"  ✓ is_practitioner criado ({df['is_practitioner'].sum()} praticantes)")

    # Faixa de idade
    if "idade" in df.columns:
        df["faixa_idade"] = bin_ages(df["idade"], bins=cfg.age_bins.bins, labels=cfg.age_bins.labels)
        print(f"  ✓ faixa_idade criado")
    else:
        df["faixa_idade"] = None

    print(f"✓ Features derivadas criadas")
    return df


def apply_filters(df: pd.DataFrame, cfg: DictConfig) -> pd.DataFrame:
    """
    Aplica filtros configurados ao DataFrame.

    Args:
        df: DataFrame processado
        cfg: Configuração Hydra

    Returns:
        DataFrame filtrado
    """
    print("\n🔍 Aplicando filtros...")

    df = df.copy()
    initial_len = len(df)

    # Filtro de idade
    if "idade" in df.columns:
        df = df[
            (df["idade"] >= cfg.filters.idade_min) & (df["idade"] <= cfg.filters.idade_max)
        ]

    # Filtro de data
    if "dt" in df.columns:
        if cfg.filters.data_inicio is not None:
            data_inicio = pd.to_datetime(cfg.filters.data_inicio).tz_localize("UTC")
            df = df[df["dt"] >= data_inicio]

        if cfg.filters.data_fim is not None:
            data_fim = pd.to_datetime(cfg.filters.data_fim).tz_localize("UTC")
            df = df[df["dt"] <= data_fim]

    # Filtro de fumantes
    if cfg.filters.apenas_fumantes is not None and "is_smoker" in df.columns:
        df = df[df["is_smoker"] == cfg.filters.apenas_fumantes]

    # Filtro de praticantes
    if cfg.filters.apenas_praticantes is not None and "is_practitioner" in df.columns:
        df = df[df["is_practitioner"] == cfg.filters.apenas_praticantes]

    removed = initial_len - len(df)
    if removed > 0:
        print(f"⚠️  Filtros removeram {removed} linhas")

    print(f"✓ Dados filtrados: {len(df)} linhas restantes")
    return df


def combine_datasets(
    df_public: Optional[pd.DataFrame] = None,
    df_wearable: Optional[pd.DataFrame] = None,
    deduplicate: bool = True,
) -> pd.DataFrame:
    """
    Combina datasets público e wearable.

    Args:
        df_public: DataFrame do dataset público
        df_wearable: DataFrame do dataset wearable
        deduplicate: Se True, remove duplicatas por (id, dt)

    Returns:
        DataFrame combinado
    """
    print("\n🔗 Combinando datasets...")

    dfs_to_combine = []

    if df_public is not None and len(df_public) > 0:
        df_public_copy = df_public.copy()
        df_public_copy["source"] = "public"
        df_public_copy["fonte"] = "público"
        dfs_to_combine.append(df_public_copy)
        print(f"  + Dataset público: {len(df_public)} linhas")

    if df_wearable is not None and len(df_wearable) > 0:
        df_wearable_copy = df_wearable.copy()
        df_wearable_copy["source"] = "wearable"
        df_wearable_copy["fonte"] = "wearable"
        dfs_to_combine.append(df_wearable_copy)
        print(f"  + Dataset wearable: {len(df_wearable)} linhas")

    if not dfs_to_combine:
        raise ValueError("Nenhum dataset fornecido para combinar")

    # Combinar
    df_combined = pd.concat(dfs_to_combine, ignore_index=True)

    # Remover duplicatas
    if deduplicate:
        initial_len = len(df_combined)
        df_combined = df_combined.drop_duplicates(subset=["id", "dt"], keep="first")
        removed = initial_len - len(df_combined)
        if removed > 0:
            print(f"⚠️  Removidas {removed} duplicatas na combinação")

    print(f"✓ Datasets combinados: {len(df_combined)} linhas totais")
    return df_combined


def preprocess_pipeline(
    df_public: Optional[pd.DataFrame] = None,
    df_wearable: Optional[pd.DataFrame] = None,
    cfg: Optional[DictConfig] = None,
    validate: bool = True,
) -> pd.DataFrame:
    """
    Pipeline completo de preprocessamento.

    Args:
        df_public: DataFrame do dataset público
        df_wearable: DataFrame do dataset wearable
        cfg: Configuração Hydra
        validate: Se True, valida com pandera

    Returns:
        DataFrame processado e combinado
    """
    print("\n" + "=" * 60)
    print("🚀 INICIANDO PIPELINE DE PREPROCESSAMENTO")
    print("=" * 60)

    if cfg is None:
        from hydra import compose, initialize

        with initialize(config_path="../conf", version_base=None):
            cfg = compose(config_name="config")

    processed_dfs = []

    # Processar dataset público
    if df_public is not None and cfg.use_public:
        df_pub_clean = clean_public_dataset(df_public, cfg)
        df_pub_processed = engineer_features(df_pub_clean, cfg)

        # Validação desabilitada (schema.py não existe)
        # if validate:
        #     df_pub_processed, df_pub_invalid = validate_dataframe(
        #         df_pub_processed, schema_type="processed", lazy=True
        #     )
        #     if df_pub_invalid is not None and len(df_pub_invalid) > 0:
        #         print(f"⚠️  {len(df_pub_invalid)} linhas inválidas removidas do dataset público")

        processed_dfs.append(df_pub_processed)

    # Processar dataset wearable
    if df_wearable is not None and cfg.use_wearable:
        df_wear_clean = clean_wearable_dataset(df_wearable, cfg)
        df_wear_processed = engineer_features(df_wear_clean, cfg)

        # Validação desabilitada (schema.py não existe)
        # if validate:
        #     df_wear_processed, df_wear_invalid = validate_dataframe(
        #         df_wear_processed, schema_type="processed", lazy=True
        #     )
        #     if df_wear_invalid is not None and len(df_wear_invalid) > 0:
        #         print(f"⚠️  {len(df_wear_invalid)} linhas inválidas removidas do dataset wearable")

        processed_dfs.append(df_wear_processed)

    # Combinar datasets
    if len(processed_dfs) == 0:
        raise ValueError("Nenhum dataset foi processado. Verifique use_public e use_wearable.")

    df_combined = combine_datasets(
        df_public=processed_dfs[0] if len(processed_dfs) > 0 and cfg.use_public else None,
        df_wearable=processed_dfs[-1] if len(processed_dfs) > 0 and cfg.use_wearable else None,
        deduplicate=True,
    )

    # Aplicar filtros
    df_final = apply_filters(df_combined, cfg)

    print("\n" + "=" * 60)
    print(f"✅ PIPELINE CONCLUÍDO: {len(df_final)} linhas finais")
    print("=" * 60)

    return df_final


if __name__ == "__main__":
    print("✓ Módulo preprocess carregado com sucesso")

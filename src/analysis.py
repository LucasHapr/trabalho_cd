"""
Módulo de análises estatísticas.

Este módulo implementa as 4 análises principais do projeto:
1. Comparação entre fumantes e não fumantes em esportes
2. Comparação de praticantes vs não praticantes de corrida (pace)
3. Comparação de prática de esportes por faixas de idade
4. Comparação da média de BPM entre praticantes e não praticantes
"""

from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from scipy import stats


def analyze_smokers_vs_nonsmokers(
    df: pd.DataFrame, sport_activities: Optional[List[str]] = None
) -> Tuple[pd.DataFrame, Dict]:
    """
    Análise 1: Comparação entre fumantes e não fumantes em esportes.

    Compara métricas de performance (pace, BPM, calorias, passos) entre
    fumantes e não fumantes que praticam atividades esportivas.

    Args:
        df: DataFrame processado
        sport_activities: Lista de atividades consideradas esportivas

    Returns:
        Tupla (df_summary, stats_dict) com:
        - df_summary: DataFrame com estatísticas agregadas
        - stats_dict: Dicionário com testes estatísticos
    """
    print("\n📊 ANÁLISE 1: Fumantes vs Não Fumantes em Esportes")
    print("=" * 60)

    if sport_activities is None:
        sport_activities = ["Running", "Walking", "Cycling", "Swimming", "Jogging", "Hiking"]

    # Filtrar apenas atividades esportivas
    if "atividade" in df.columns:
        pattern = "|".join(sport_activities)
        df_sports = df[df["atividade"].str.contains(pattern, case=False, na=False)].copy()
    else:
        # Se não tem coluna atividade, considerar todos que são praticantes
        df_sports = df[df["is_practitioner"]].copy()

    print(f"  Linhas com atividades esportivas: {len(df_sports)}")

    if len(df_sports) == 0:
        print("⚠️  Nenhuma linha com atividades esportivas encontrada")
        return pd.DataFrame(), {}

    # Agrupar por status de fumante
    metrics = ["pace_min_km", "bpm", "calorias_kcal", "passos"]
    available_metrics = [m for m in metrics if m in df_sports.columns]

    # Calcular estatísticas descritivas
    summary_data = []

    for is_smoker_val in [False, True]:
        df_group = df_sports[df_sports["is_smoker"] == is_smoker_val]
        group_name = "Fumante" if is_smoker_val else "Não Fumante"

        row = {"grupo": group_name, "n": len(df_group)}

        for metric in available_metrics:
            values = df_group[metric].dropna()
            if len(values) > 0:
                row[f"{metric}_mean"] = values.mean()
                row[f"{metric}_median"] = values.median()
                row[f"{metric}_std"] = values.std()
                row[f"{metric}_min"] = values.min()
                row[f"{metric}_max"] = values.max()
            else:
                row[f"{metric}_mean"] = np.nan
                row[f"{metric}_median"] = np.nan
                row[f"{metric}_std"] = np.nan
                row[f"{metric}_min"] = np.nan
                row[f"{metric}_max"] = np.nan

        summary_data.append(row)

    df_summary = pd.DataFrame(summary_data)

    # Testes estatísticos (Mann-Whitney U test)
    stats_dict = {}

    for metric in available_metrics:
        smokers = df_sports[df_sports["is_smoker"]][metric].dropna()
        non_smokers = df_sports[~df_sports["is_smoker"]][metric].dropna()

        if len(smokers) > 0 and len(non_smokers) > 0:
            statistic, pvalue = stats.mannwhitneyu(smokers, non_smokers, alternative="two-sided")
            stats_dict[metric] = {"statistic": statistic, "pvalue": pvalue, "significant": pvalue < 0.05}

            sig_marker = "***" if pvalue < 0.001 else "**" if pvalue < 0.01 else "*" if pvalue < 0.05 else "ns"
            print(f"  {metric}: p-value = {pvalue:.4f} {sig_marker}")

    print("\n✓ Análise de fumantes vs não fumantes concluída")
    return df_summary, stats_dict


def analyze_runners_vs_nonrunners(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
    """
    Análise 2: Comparação de praticantes vs não praticantes de corrida (pace).

    Compara o pace (ritmo) e outras métricas entre quem pratica corrida
    e quem não pratica.

    Args:
        df: DataFrame processado

    Returns:
        Tupla (df_summary, stats_dict) com estatísticas e testes
    """
    print("\n📊 ANÁLISE 2: Praticantes vs Não Praticantes de Corrida")
    print("=" * 60)

    if "is_runner" not in df.columns:
        print("⚠️  Coluna 'is_runner' não encontrada")
        return pd.DataFrame(), {}

    # Filtrar apenas quem tem pace válido
    df_with_pace = df[df["pace_min_km"].notna()].copy()
    print(f"  Linhas com pace válido: {len(df_with_pace)}")

    metrics = ["pace_min_km", "bpm", "calorias_kcal", "passos", "distancia_km", "duracao_min"]
    available_metrics = [m for m in metrics if m in df_with_pace.columns]

    # Calcular estatísticas descritivas
    summary_data = []

    for is_runner_val in [False, True]:
        df_group = df_with_pace[df_with_pace["is_runner"] == is_runner_val]
        group_name = "Runner" if is_runner_val else "Não Runner"

        row = {"grupo": group_name, "n": len(df_group)}

        for metric in available_metrics:
            values = df_group[metric].dropna()
            if len(values) > 0:
                row[f"{metric}_mean"] = values.mean()
                row[f"{metric}_median"] = values.median()
                row[f"{metric}_std"] = values.std()
                row[f"{metric}_q25"] = values.quantile(0.25)
                row[f"{metric}_q75"] = values.quantile(0.75)
            else:
                for stat in ["mean", "median", "std", "q25", "q75"]:
                    row[f"{metric}_{stat}"] = np.nan

        summary_data.append(row)

    df_summary = pd.DataFrame(summary_data)

    # Testes estatísticos
    stats_dict = {}

    for metric in available_metrics:
        runners = df_with_pace[df_with_pace["is_runner"]][metric].dropna()
        non_runners = df_with_pace[~df_with_pace["is_runner"]][metric].dropna()

        if len(runners) > 0 and len(non_runners) > 0:
            statistic, pvalue = stats.mannwhitneyu(runners, non_runners, alternative="two-sided")
            stats_dict[metric] = {"statistic": statistic, "pvalue": pvalue, "significant": pvalue < 0.05}

            sig_marker = "***" if pvalue < 0.001 else "**" if pvalue < 0.01 else "*" if pvalue < 0.05 else "ns"
            print(f"  {metric}: p-value = {pvalue:.4f} {sig_marker}")

    print("\n✓ Análise de runners vs não runners concluída")
    return df_summary, stats_dict


def analyze_practice_by_age(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Análise 3: Comparação de prática de esportes por faixas de idade.

    Analisa a taxa de praticantes e métricas de atividade por faixa etária.

    Args:
        df: DataFrame processado

    Returns:
        Tupla (df_rates, df_metrics) com:
        - df_rates: Taxa de praticantes por faixa de idade
        - df_metrics: Métricas médias por faixa de idade
    """
    print("\n📊 ANÁLISE 3: Prática de Esportes por Faixas de Idade")
    print("=" * 60)

    if "faixa_idade" not in df.columns:
        print("⚠️  Coluna 'faixa_idade' não encontrada")
        return pd.DataFrame(), pd.DataFrame()

    # Taxa de praticantes por faixa
    df_rates = (
        df.groupby("faixa_idade")
        .agg(
            total=("is_practitioner", "count"),
            praticantes=("is_practitioner", "sum"),
            taxa_praticantes=("is_practitioner", "mean"),
        )
        .reset_index()
    )

    df_rates["taxa_praticantes_pct"] = df_rates["taxa_praticantes"] * 100

    print("\nTaxa de praticantes por faixa de idade:")
    print(df_rates[["faixa_idade", "total", "praticantes", "taxa_praticantes_pct"]])

    # Métricas médias por faixa (apenas praticantes)
    df_practitioners = df[df["is_practitioner"]].copy()

    metrics = ["duracao_min", "distancia_km", "calorias_kcal", "bpm", "passos", "pace_min_km"]
    available_metrics = [m for m in metrics if m in df_practitioners.columns]

    agg_dict = {m: ["mean", "median", "std", "count"] for m in available_metrics}

    df_metrics = df_practitioners.groupby("faixa_idade").agg(agg_dict).reset_index()

    # Flatten multi-level columns
    df_metrics.columns = [
        "_".join(col).strip("_") if col[1] else col[0] for col in df_metrics.columns.values
    ]

    print("\n✓ Análise de prática por idade concluída")
    return df_rates, df_metrics


def analyze_bpm_practitioners_vs_nonpractitioners(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
    """
    Análise 4: Comparação da média de BPM entre praticantes e não praticantes.

    Compara o BPM médio entre quem pratica e quem não pratica atividades físicas,
    incluindo análise por faixa etária.

    Args:
        df: DataFrame processado

    Returns:
        Tupla (df_summary, stats_dict) com estatísticas e testes
    """
    print("\n📊 ANÁLISE 4: BPM Praticantes vs Não Praticantes")
    print("=" * 60)

    if "bpm" not in df.columns:
        print("⚠️  Coluna 'bpm' não encontrada")
        return pd.DataFrame(), {}

    # Filtrar apenas com BPM válido
    df_with_bpm = df[df["bpm"].notna()].copy()
    print(f"  Linhas com BPM válido: {len(df_with_bpm)}")

    # Estatísticas gerais
    summary_data = []

    for is_pract_val in [False, True]:
        df_group = df_with_bpm[df_with_bpm["is_practitioner"] == is_pract_val]
        group_name = "Praticante" if is_pract_val else "Não Praticante"

        bpm_values = df_group["bpm"].dropna()

        if len(bpm_values) > 0:
            summary_data.append(
                {
                    "grupo": group_name,
                    "n": len(bpm_values),
                    "bpm_mean": bpm_values.mean(),
                    "bpm_median": bpm_values.median(),
                    "bpm_std": bpm_values.std(),
                    "bpm_min": bpm_values.min(),
                    "bpm_max": bpm_values.max(),
                }
            )

    df_summary = pd.DataFrame(summary_data)

    print("\nEstatísticas gerais de BPM:")
    print(df_summary)

    # Teste estatístico
    practitioners = df_with_bpm[df_with_bpm["is_practitioner"]]["bpm"].dropna()
    non_practitioners = df_with_bpm[~df_with_bpm["is_practitioner"]]["bpm"].dropna()

    stats_dict = {}

    if len(practitioners) > 0 and len(non_practitioners) > 0:
        statistic, pvalue = stats.mannwhitneyu(
            practitioners, non_practitioners, alternative="two-sided"
        )
        stats_dict["overall"] = {
            "statistic": statistic,
            "pvalue": pvalue,
            "significant": pvalue < 0.05,
        }

        sig_marker = "***" if pvalue < 0.001 else "**" if pvalue < 0.01 else "*" if pvalue < 0.05 else "ns"
        print(f"\nTeste Mann-Whitney U: p-value = {pvalue:.4f} {sig_marker}")

    # Análise por faixa de idade
    if "faixa_idade" in df_with_bpm.columns:
        print("\nBPM médio por faixa de idade e status de praticante:")

        df_by_age = (
            df_with_bpm.groupby(["faixa_idade", "is_practitioner"])["bpm"]
            .agg(["mean", "median", "count"])
            .reset_index()
        )

        df_by_age["grupo"] = df_by_age["is_practitioner"].map(
            {True: "Praticante", False: "Não Praticante"}
        )

        # Pivot para visualização
        df_pivot = df_by_age.pivot(index="faixa_idade", columns="grupo", values="mean")

        print(df_pivot)

        stats_dict["by_age"] = df_by_age

    print("\n✓ Análise de BPM praticantes vs não praticantes concluída")
    return df_summary, stats_dict


def run_all_analyses(df: pd.DataFrame, sport_activities: Optional[List[str]] = None) -> Dict:
    """
    Executa todas as 4 análises principais.

    Args:
        df: DataFrame processado
        sport_activities: Lista de atividades esportivas

    Returns:
        Dicionário com resultados de todas as análises
    """
    print("\n" + "=" * 60)
    print("🚀 EXECUTANDO TODAS AS ANÁLISES")
    print("=" * 60)

    results = {}

    # Análise 1
    results["smokers_vs_nonsmokers"] = {}
    results["smokers_vs_nonsmokers"]["summary"], results["smokers_vs_nonsmokers"]["stats"] = (
        analyze_smokers_vs_nonsmokers(df, sport_activities)
    )

    # Análise 2
    results["runners_vs_nonrunners"] = {}
    results["runners_vs_nonrunners"]["summary"], results["runners_vs_nonrunners"]["stats"] = (
        analyze_runners_vs_nonrunners(df)
    )

    # Análise 3
    results["practice_by_age"] = {}
    results["practice_by_age"]["rates"], results["practice_by_age"]["metrics"] = (
        analyze_practice_by_age(df)
    )

    # Análise 4
    results["bpm_practitioners"] = {}
    results["bpm_practitioners"]["summary"], results["bpm_practitioners"]["stats"] = (
        analyze_bpm_practitioners_vs_nonpractitioners(df)
    )

    print("\n" + "=" * 60)
    print("✅ TODAS AS ANÁLISES CONCLUÍDAS")
    print("=" * 60)

    return results


if __name__ == "__main__":
    print("✓ Módulo analysis carregado com sucesso")

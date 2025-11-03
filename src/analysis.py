"""
Módulo de análises estatísticas - Versão otimizada para fitlife_clean.csv

Este módulo contém funções para realizar as 4 análises principais:
1. Fumantes vs não fumantes (médias/medianas de pace_min_km, bpm, calorias_kcal, passos)
2. Praticantes de corrida (is_runner=True) vs não praticantes (distribuição de pace_min_km)
3. Prática de esportes por faixas de idade (taxa de is_practitioner e média duracao_min)
4. Média de bpm entre is_practitioner vs ~is_practitioner, segmentada por faixa_idade

Uso batch: python -m src.analysis_v2
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from scipy import stats


def analyze_smokers_vs_nonsmokers(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
    """
    Análise 1: Fumantes vs Não Fumantes.
    
    Compara médias e medianas de bpm e calorias_kcal
    entre fumantes (is_smoker=True) e não fumantes (is_smoker=False).
    
    Args:
        df: DataFrame com colunas [is_smoker, bpm, calorias_kcal]
    
    Returns:
        Tuple contendo:
        - DataFrame com métricas agregadas por grupo (fumante/não fumante)
        - Dict com testes estatísticos (Mann-Whitney U test p-values)
    """
    # Filtrar apenas linhas válidas
    df_valid = df[df['is_smoker'].notna()].copy()
    
    # Métricas a analisar (apenas as disponíveis no dataset)
    metrics = ['bpm', 'calorias_kcal']
    
    # Agregar por grupo
    results = []
    for is_smoker in [True, False]:
        df_group = df_valid[df_valid['is_smoker'] == is_smoker]
        
        row = {
            'grupo': 'Fumante' if is_smoker else 'Não Fumante',
            'n': len(df_group)
        }
        
        for metric in metrics:
            data = df_group[metric].dropna()
            if len(data) > 0:
                row[f'{metric}_mean'] = data.mean()
                row[f'{metric}_median'] = data.median()
                row[f'{metric}_std'] = data.std()
            else:
                row[f'{metric}_mean'] = np.nan
                row[f'{metric}_median'] = np.nan
                row[f'{metric}_std'] = np.nan
        
        results.append(row)
    
    df_summary = pd.DataFrame(results)
    
    # Testes estatísticos (Mann-Whitney U)
    stats_dict = {'test': 'Mann-Whitney U', 'metrics': {}}
    
    smokers = df_valid[df_valid['is_smoker'] == True]
    non_smokers = df_valid[df_valid['is_smoker'] == False]
    
    for metric in metrics:
        data_smokers = smokers[metric].dropna()
        data_non_smokers = non_smokers[metric].dropna()
        
        if len(data_smokers) > 0 and len(data_non_smokers) > 0:
            statistic, p_value = stats.mannwhitneyu(data_smokers, data_non_smokers, alternative='two-sided')
            stats_dict['metrics'][metric] = {
                'statistic': float(statistic),
                'p_value': float(p_value),
                'significant': p_value < 0.05
            }
    
    return df_summary, stats_dict


def analyze_runners_vs_nonrunners(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
    """
    Análise 2: Praticantes de Corrida vs Não Praticantes.
    
    Compara a distribuição de BPM e calorias entre is_runner=True e is_runner=False
    (já que pace_min_km não está disponível no dataset público).
    
    Args:
        df: DataFrame com colunas [is_runner, bpm, calorias_kcal]
    
    Returns:
        Tuple contendo:
        - DataFrame com estatísticas descritivas por grupo
        - Dict com testes estatísticos (Mann-Whitney U, Kolmogorov-Smirnov)
    """
    # Filtrar apenas linhas válidas
    df_valid = df[df['is_runner'].notna()].copy()
    
    # Agregar por grupo
    results = []
    for is_runner in [True, False]:
        df_group = df_valid[df_valid['is_runner'] == is_runner]
        
        bpm_data = df_group['bpm'].dropna()
        cal_data = df_group['calorias_kcal'].dropna()
        
        if len(bpm_data) > 0:
            results.append({
                'grupo': 'Corredor' if is_runner else 'Não Corredor',
                'n': len(df_group),
                'bpm_mean': bpm_data.mean(),
                'bpm_median': bpm_data.median(),
                'bpm_std': bpm_data.std(),
                'bpm_min': bpm_data.min(),
                'bpm_max': bpm_data.max(),
                'calorias_mean': cal_data.mean() if len(cal_data) > 0 else np.nan,
                'calorias_median': cal_data.median() if len(cal_data) > 0 else np.nan,
                'calorias_std': cal_data.std() if len(cal_data) > 0 else np.nan
            })
    
    df_summary = pd.DataFrame(results)
    
    # Testes estatísticos
    stats_dict = {}
    
    for metric in ['bpm', 'calorias_kcal']:
        runners_data = df_valid[df_valid['is_runner'] == True][metric].dropna()
        non_runners_data = df_valid[df_valid['is_runner'] == False][metric].dropna()
        
        if len(runners_data) > 0 and len(non_runners_data) > 0:
            # Mann-Whitney U test
            mw_stat, mw_pval = stats.mannwhitneyu(runners_data, non_runners_data, alternative='two-sided')
            
            # Kolmogorov-Smirnov test (compara distribuições)
            ks_stat, ks_pval = stats.ks_2samp(runners_data, non_runners_data)
            
            stats_dict[metric] = {
                'mann_whitney': {
                    'statistic': float(mw_stat),
                    'p_value': float(mw_pval),
                    'significant': mw_pval < 0.05
                },
                'kolmogorov_smirnov': {
                    'statistic': float(ks_stat),
                    'p_value': float(ks_pval),
                    'significant': ks_pval < 0.05
                }
            }
    
    return df_summary, stats_dict


def analyze_practice_by_age(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
    """
    Análise 3: Prática de Esportes por Faixas de Idade.
    
    Analisa a taxa de is_practitioner e média de BPM/calorias por faixa_idade
    (duracao_min não está disponível no dataset público).
    
    Args:
        df: DataFrame com colunas [faixa_idade, is_practitioner, bpm, calorias_kcal]
    
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
    # Filtrar apenas valores True, ignorando NaN
    df_practitioners = df[df["is_practitioner"] == True].copy()

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


def analyze_bpm_practitioners_vs_nonpractitioners(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, Dict]:
    """
    Análise 4: Média de BPM entre Praticantes vs Não Praticantes.
    
    Compara a média de BPM entre is_practitioner=True e is_practitioner=False,
    tanto globalmente quanto segmentada por faixa_idade.
    
    Args:
        df: DataFrame com colunas [is_practitioner, bpm, faixa_idade]
    
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
    practitioners = df_with_bpm[df_with_bpm["is_practitioner"] == True]["bpm"].dropna()
    non_practitioners = df_with_bpm[df_with_bpm["is_practitioner"] == False]["bpm"].dropna()

    stats_dict = {}
    
    if len(practitioners) > 0 and len(non_practitioners) > 0:
        # Teste t (assumindo normalidade para BPM)
        t_stat, t_pval = stats.ttest_ind(practitioners, non_practitioners)
        
        # Mann-Whitney U (não paramétrico, mais robusto)
        mw_stat, mw_pval = stats.mannwhitneyu(practitioners, non_practitioners, alternative='two-sided')
        
        # Cohen's d (tamanho do efeito)
        cohens_d = (practitioners.mean() - non_practitioners.mean()) / np.sqrt(
            ((len(practitioners) - 1) * practitioners.std()**2 + 
             (len(non_practitioners) - 1) * non_practitioners.std()**2) / 
            (len(practitioners) + len(non_practitioners) - 2)
        )
        
        stats_dict = {
            't_test': {
                'statistic': float(t_stat),
                'p_value': float(t_pval),
                'significant': t_pval < 0.05
            },
            'mann_whitney': {
                'statistic': float(mw_stat),
                'p_value': float(mw_pval),
                'significant': mw_pval < 0.05
            },
            'cohens_d': float(cohens_d),
            'effect_size': 'small' if abs(cohens_d) < 0.5 else ('medium' if abs(cohens_d) < 0.8 else 'large')
        }
    
    return df_global, df_by_age, stats_dict


# Função principal para execução batch
def main():
    """
    Executa todas as 4 análises e salva os resultados.
    
    Uso: python -m src.analysis_v2
    """
    print("=" * 80)
    print("EXECUTANDO ANÁLISES - BATCH MODE")
    print("=" * 80)
    
    # Carregar dados
    print("\n📖 Carregando dataset...")
    data_path = Path("data/external/fitlife_clean.csv")
    
    if not data_path.exists():
        print(f"❌ Arquivo não encontrado: {data_path}")
        return
    
    df = pd.read_csv(data_path)
    print(f"✓ Dataset carregado: {len(df):,} linhas, {len(df.columns)} colunas")
    
    # Criar diretório de resultados
    results_dir = Path("reports/analysis_results")
    results_dir.mkdir(parents=True, exist_ok=True)
    
    # Análise 1
    print("\n" + "=" * 80)
    print("📊 ANÁLISE 1: Fumantes vs Não Fumantes")
    print("=" * 80)
    df_smokers, stats_smokers = analyze_smokers_vs_nonsmokers(df)
    print("\nResultados:")
    print(df_smokers.to_string(index=False))
    print(f"\nTestes estatísticos:")
    for metric, result in stats_smokers['metrics'].items():
        sig = "***" if result['significant'] else "ns"
        print(f"  {metric}: p-value = {result['p_value']:.4f} {sig}")
    
    df_smokers.to_csv(results_dir / "analise1_fumantes.csv", index=False)
    
    # Análise 2
    print("\n" + "=" * 80)
    print("🏃 ANÁLISE 2: Praticantes de Corrida vs Não Praticantes")
    print("=" * 80)
    df_runners, stats_runners = analyze_runners_vs_nonrunners(df)
    print("\nResultados:")
    print(df_runners.to_string(index=False))
    print(f"\nTestes estatísticos:")
    for metric, tests in stats_runners.items():
        print(f"  {metric}:")
        print(f"    Mann-Whitney U: p-value = {tests['mann_whitney']['p_value']:.4f}")
        print(f"    Kolmogorov-Smirnov: p-value = {tests['kolmogorov_smirnov']['p_value']:.4f}")
    
    df_runners.to_csv(results_dir / "analise2_runners.csv", index=False)
    
    # Análise 3
    print("\n" + "=" * 80)
    print("👥 ANÁLISE 3: Prática de Esportes por Faixas de Idade")
    print("=" * 80)
    df_age, stats_age = analyze_practice_by_age(df)
    print("\nResultados:")
    print(df_age.to_string(index=False))
    print(f"\nTaxa global de praticantes: {stats_age['taxa_global_pct']:.1f}%")
    if stats_age['chi2_test']:
        print(f"Chi-quadrado: p-value = {stats_age['chi2_test']['p_value']:.4f}")
    
    df_age.to_csv(results_dir / "analise3_idade.csv", index=False)
    
    # Análise 4
    print("\n" + "=" * 80)
    print("💓 ANÁLISE 4: BPM Praticantes vs Não Praticantes")
    print("=" * 80)
    df_bpm_global, df_bpm_age, stats_bpm = analyze_bpm_practitioners_vs_nonpractitioners(df)
    print("\nResultados Globais:")
    print(df_bpm_global.to_string(index=False))
    print("\nResultados por Faixa de Idade:")
    print(df_bpm_age.to_string(index=False))
    print(f"\nT-test: p-value = {stats_bpm['t_test']['p_value']:.4f}")
    print(f"Cohen's d: {stats_bpm['cohens_d']:.3f} ({stats_bpm['effect_size']} effect)")
    
    df_bpm_global.to_csv(results_dir / "analise4_bpm_global.csv", index=False)
    df_bpm_age.to_csv(results_dir / "analise4_bpm_por_idade.csv", index=False)
    
    print("\n" + "=" * 80)
    print("✅ ANÁLISES CONCLUÍDAS!")
    print(f"📁 Resultados salvos em: {results_dir}")
    print("=" * 80)


if __name__ == "__main__":
    main()

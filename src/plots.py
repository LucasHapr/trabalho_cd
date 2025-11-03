"""
Módulo de visualizações para análise de fitness - Otimizado para fitlife_clean.csv

Contém funções para criar visualizações interativas (Plotly) e estáticas (Seaborn/Matplotlib)
para as 4 análises principais.

Uso batch: python -m src.plots_v2
"""

from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns

# Configurações
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.bbox'] = 'tight'

# Paleta de cores
COLOR_PALETTE = px.colors.qualitative.Set2


# =============================================================================
# ANÁLISE 1: FUMANTES VS NÃO FUMANTES
# =============================================================================

def plot_smokers_comparison_boxplot(
    df: pd.DataFrame,
    metric: str = 'bpm',
    save_path: Optional[Path] = None
) -> go.Figure:
    """
    Boxplot interativo comparando fumantes vs não fumantes.
    
    Args:
        df: DataFrame com colunas [is_smoker, metric]
        metric: Métrica a plotar ('bpm' ou 'calorias_kcal')
        save_path: Caminho para salvar HTML (opcional)
    
    Returns:
        Figura Plotly
    """
    df_plot = df[df[metric].notna()].copy()
    df_plot['Grupo'] = df_plot['is_smoker'].map({True: 'Fumante', False: 'Não Fumante'})
    
    # Mapear labels mais descritivos
    metric_labels = {
        'bpm': 'BPM (Batimentos por Minuto)',
        'pace_min_km': 'Pace (min/km)',
        'calorias_kcal': 'Calorias (kcal)',
        'calorias': 'Calorias (kcal)',
        'passos': 'Passos',
        'distancia_km': 'Distância (km)'
    }
    
    fig = px.box(
        df_plot,
        x='Grupo',
        y=metric,
        color='Grupo',
        title=f'Comparação: {metric_labels.get(metric, metric)}',
        labels={metric: metric_labels.get(metric, metric), 'Grupo': ''},
        color_discrete_map={'Fumante': '#e74c3c', 'Não Fumante': '#2ecc71'}
    )
    
    fig.update_layout(
        template='plotly_white',
        showlegend=False,
        height=500,
        font=dict(size=12)
    )
    
    if save_path:
        fig.write_html(save_path)
    
    return fig


def plot_smokers_comparison_violin(
    df: pd.DataFrame,
    metric: str = 'bpm',
    save_path: Optional[Path] = None
) -> go.Figure:
    """
    Violin plot interativo comparando fumantes vs não fumantes.
    """
    df_plot = df[df[metric].notna()].copy()
    df_plot['Grupo'] = df_plot['is_smoker'].map({True: 'Fumante', False: 'Não Fumante'})
    
    # Mapear labels mais descritivos
    metric_labels = {
        'bpm': 'BPM (Batimentos por Minuto)',
        'pace_min_km': 'Pace (min/km)',
        'calorias_kcal': 'Calorias (kcal)',
        'calorias': 'Calorias (kcal)',
        'passos': 'Passos',
        'distancia_km': 'Distância (km)'
    }
    
    fig = px.violin(
        df_plot,
        x='Grupo',
        y=metric,
        color='Grupo',
        box=True,
        title=f'Distribuição Detalhada: {metric_labels.get(metric, metric)}',
        labels={metric: metric_labels.get(metric, metric), 'Grupo': ''},
        color_discrete_map={'Fumante': '#e74c3c', 'Não Fumante': '#2ecc71'}
    )
    
    fig.update_layout(
        template='plotly_white',
        showlegend=False,
        height=500,
        font=dict(size=12)
    )
    
    if save_path:
        fig.write_html(save_path)
    
    return fig


def plot_smokers_comparison_static(
    df: pd.DataFrame,
    save_path: Optional[Path] = None
):
    """
    Versão estática do plot de fumantes (PNG).
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    df_plot = df.copy()
    df_plot['Grupo'] = df_plot['is_smoker'].map({True: 'Fumante', False: 'Não Fumante'})
    
    # BPM
    sns.boxplot(data=df_plot, x='Grupo', y='bpm', ax=axes[0], palette=['#e74c3c', '#3498db'])
    axes[0].set_title('Distribuição de BPM')
    axes[0].set_ylabel('BPM')
    
    # Calorias
    sns.boxplot(data=df_plot, x='Grupo', y='calorias_kcal', ax=axes[1], palette=['#e74c3c', '#3498db'])
    axes[1].set_title('Distribuição de Calorias')
    axes[1].set_ylabel('Calorias (kcal)')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        return fig


# =============================================================================
# ANÁLISE 2: RUNNERS VS NÃO RUNNERS
# =============================================================================

def plot_runners_comparison_boxplot(
    df: pd.DataFrame,
    metric: str = 'bpm',
    save_path: Optional[Path] = None
) -> go.Figure:
    """
    Boxplot interativo comparando runners vs não runners.
    """
    df_plot = df[df[metric].notna()].copy()
    df_plot['Grupo'] = df_plot['is_runner'].map({True: 'Corredor', False: 'Não Corredor'})
    
    # Mapear labels mais descritivos
    metric_labels = {
        'bpm': 'BPM (Batimentos por Minuto)',
        'pace_min_km': 'Pace (min/km)',
        'calorias_kcal': 'Calorias (kcal)',
        'calorias': 'Calorias (kcal)',
        'passos': 'Passos',
        'distancia_km': 'Distância (km)'
    }
    
    fig = px.box(
        df_plot,
        x='Grupo',
        y=metric,
        color='Grupo',
        title=f'Comparação: {metric_labels.get(metric, metric)}',
        labels={metric: metric_labels.get(metric, metric), 'Grupo': ''},
        color_discrete_map={'Corredor': '#3498db', 'Não Corredor': '#95a5a6'}
    )
    
    fig.update_layout(
        template='plotly_white',
        showlegend=False,
        height=500,
        font=dict(size=12)
    )
    
    if save_path:
        fig.write_html(save_path)
    
    return fig


def plot_runners_comparison_histogram(
    df: pd.DataFrame,
    metric: str = 'calorias_kcal',
    save_path: Optional[Path] = None
) -> go.Figure:
    """
    Histograma sobreposto comparando runners vs não runners.
    """
    df_plot = df[df[metric].notna()].copy()
    df_plot['Grupo'] = df_plot['is_runner'].map({True: 'Corredor', False: 'Não Corredor'})
    
    # Mapear labels mais descritivos
    metric_labels = {
        'bpm': 'BPM (Batimentos por Minuto)',
        'pace_min_km': 'Pace (min/km)',
        'calorias_kcal': 'Calorias (kcal)',
        'calorias': 'Calorias (kcal)',
        'passos': 'Passos',
        'distancia_km': 'Distância (km)'
    }
    
    fig = px.histogram(
        df_plot,
        x=metric,
        color='Grupo',
        nbins=50,
        title=f'Distribuição de Frequência: {metric_labels.get(metric, metric)}',
        labels={metric: metric_labels.get(metric, metric), 'count': 'Frequência'},
        color_discrete_map={'Corredor': '#3498db', 'Não Corredor': '#95a5a6'},
        barmode='overlay',
        opacity=0.75
    )

    fig.update_layout(
        template='plotly_white',
        height=500,
        font=dict(size=12)
    )

    return fig


def plot_runners_comparison_histogram_seaborn(
    df: pd.DataFrame, metric: str = "pace_min_km"
) -> plt.Figure:
    """
    Histograma com KDE comparando runners vs não runners (Seaborn).

    Args:
        df: DataFrame processado
        metric: Métrica a comparar

    Returns:
        Figura Matplotlib
    """
    df_plot = df[df[metric].notna()].copy()
    df_plot["Status"] = df_plot["is_runner"].map({True: "Runner", False: "Não Runner"})

    fig, ax = plt.subplots(figsize=(12, 6))

    for status in df_plot["Status"].unique():
        data = df_plot[df_plot["Status"] == status][metric]
        sns.histplot(data, kde=True, label=status, alpha=0.5, ax=ax)

    ax.set_title(
        f"Distribuição de {metric}: Runners vs Não Runners", fontsize=14, fontweight="bold"
    )
    ax.set_xlabel(metric.replace("_", " ").title(), fontsize=12)
    ax.set_ylabel("Frequência", fontsize=12)
    ax.legend()

    plt.tight_layout()
    return fig


# ============================================================================
# ANÁLISE 3: Prática por Faixas de Idade
# ============================================================================


def plot_practice_by_age_bars_plotly(df_rates: pd.DataFrame) -> go.Figure:
    """
    Gráfico de barras com taxa de praticantes por faixa de idade (Plotly).

    Args:
        df_rates: DataFrame com taxas por faixa de idade

    Returns:
        Figura Plotly
    """
    fig = go.Figure()
    
    # Converter para numérico e preencher NaN com 0
    taxa_pct = pd.to_numeric(df_rates["taxa_praticantes_pct"], errors='coerce').fillna(0)
    text_values = taxa_pct.round(1).astype(str) + "%"

    fig.add_trace(
        go.Bar(
            x=df_rates["faixa_idade"],
            y=taxa_pct,
            marker_color='#3498db',
            text=text_values,
            textposition="outside",
            marker=dict(
                line=dict(color='#2c3e50', width=1)
            )
        )
    )

    fig.update_layout(
        title='Taxa de Praticantes por Faixa Etária',
        xaxis_title='Faixa de Idade',
        yaxis_title='Taxa de Praticantes (%)',
        template='plotly_white',
        height=500,
        font=dict(size=12),
        yaxis=dict(range=[0, max(taxa_pct) * 1.15])  # Adicionar espaço para labels
    )
    
    return fig


def plot_runners_comparison_static(
    df: pd.DataFrame,
    save_path: Optional[Path] = None
):
    """
    Versão estática do plot de runners (PNG).
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    df_plot = df.copy()
    df_plot['Grupo'] = df_plot['is_runner'].map({True: 'Corredor', False: 'Não Corredor'})
    
    # BPM
    sns.violinplot(data=df_plot, x='Grupo', y='bpm', ax=axes[0], palette=['#2ecc71', '#95a5a6'])
    axes[0].set_title('Distribuição de BPM')
    axes[0].set_ylabel('BPM')
    
    # Calorias
    sns.violinplot(data=df_plot, x='Grupo', y='calorias_kcal', ax=axes[1], palette=['#2ecc71', '#95a5a6'])
    axes[1].set_title('Distribuição de Calorias')
    axes[1].set_ylabel('Calorias (kcal)')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        return fig


# =============================================================================
# ANÁLISE 3: PRÁTICA POR FAIXA DE IDADE
# =============================================================================

def plot_practice_by_age_bars(
    df_summary: pd.DataFrame,
    save_path: Optional[Path] = None
) -> go.Figure:
    """
    Gráfico de barras com taxa de praticantes por faixa de idade.
    
    Args:
        df_summary: DataFrame resultado de analyze_practice_by_age()
        save_path: Caminho para salvar HTML (opcional)
    """
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df_summary['faixa_idade'],
        y=df_summary['taxa_praticantes_pct'],
        text=df_summary['taxa_praticantes_pct'].round(1),
        texttemplate='%{text}%',
        textposition='outside',
        marker_color='#9b59b6',
        name='Taxa de Praticantes'
    ))
    
    fig.update_layout(
        title='Taxa de Praticantes de Esportes por Faixa de Idade',
        xaxis_title='Faixa de Idade',
        yaxis_title='Taxa de Praticantes (%)',
        template='plotly_white',
        showlegend=False,
        height=500
    )
    
    if save_path:
        fig.write_html(save_path)
    
    return fig


def plot_practice_by_age_stacked(
    df_summary: pd.DataFrame,
    save_path: Optional[Path] = None
) -> go.Figure:
    """
    Gráfico de barras empilhadas mostrando praticantes vs não praticantes.
    """
    df_plot = df_summary.copy()
    
    # Verificar quais colunas existem (podem ser 'total'/'praticantes' ou 'n_total'/'n_praticantes')
    total_col = 'n_total' if 'n_total' in df_plot.columns else 'total'
    prat_col = 'n_praticantes' if 'n_praticantes' in df_plot.columns else 'praticantes'
    
    df_plot['nao_praticantes'] = df_plot[total_col] - df_plot[prat_col]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df_plot['faixa_idade'],
        y=df_plot[prat_col],
        name='Praticantes',
        marker_color='#2ecc71'
    ))
    
    fig.add_trace(go.Bar(
        x=df_plot['faixa_idade'],
        y=df_plot['nao_praticantes'],
        name='Não Praticantes',
        marker_color='#e74c3c'
    ))
    
    fig.update_layout(
        title='Número de Praticantes e Não Praticantes por Faixa de Idade',
        xaxis_title='Faixa de Idade',
        yaxis_title='Número de Pessoas',
        template='plotly_white',
        barmode='stack',
        height=500
    )
    
    return fig


def plot_practice_by_age_static(
    df_summary: pd.DataFrame,
    save_path: Optional[Path] = None
):
    """
    Versão estática do plot de prática por idade (PNG).
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Taxa de praticantes
    axes[0].bar(df_summary['faixa_idade'], df_summary['taxa_praticantes_pct'], color='#9b59b6')
    axes[0].set_title('Taxa de Praticantes por Faixa de Idade')
    axes[0].set_xlabel('Faixa de Idade')
    axes[0].set_ylabel('Taxa de Praticantes (%)')
    axes[0].tick_params(axis='x', rotation=45)
    
    # Média de BPM
    axes[1].plot(df_summary['faixa_idade'], df_summary['bpm_mean'], marker='o', color='#3498db', linewidth=2)
    axes[1].set_title('BPM Médio por Faixa de Idade')
    axes[1].set_xlabel('Faixa de Idade')
    axes[1].set_ylabel('BPM Médio')
    axes[1].tick_params(axis='x', rotation=45)
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        return fig


# =============================================================================
# ANÁLISE 4: BPM PRATICANTES VS NÃO PRATICANTES
# =============================================================================

def plot_bpm_practitioners_comparison(
    df: pd.DataFrame,
    save_path: Optional[Path] = None
) -> go.Figure:
    """
    Gráfico de barras comparando BPM médio entre praticantes e não praticantes.
    """
    # Criar resumo de dados
    df_with_bpm = df[df["bpm"].notna()].copy()
    
    summary_data = []
    for is_pract_val in [False, True]:
        df_group = df_with_bpm[df_with_bpm["is_practitioner"] == is_pract_val]
        group_name = "Praticante" if is_pract_val else "Não Praticante"
        bpm_values = df_group["bpm"].dropna()
        
        if len(bpm_values) > 0:
            summary_data.append({
                "grupo": group_name,
                "bpm_mean": bpm_values.mean(),
                "bpm_std": bpm_values.std(),
            })
    
    df_global = pd.DataFrame(summary_data)
    
    if df_global.empty:
        # Retornar figura vazia se não houver dados
        fig = go.Figure()
        fig.update_layout(title='Sem dados disponíveis')
        return fig
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df_global['grupo'],
        y=df_global['bpm_mean'],
        text=df_global['bpm_mean'].round(1),
        texttemplate='%{text}',
        textposition='outside',
        marker_color=['#e74c3c', '#2ecc71'],
        error_y=dict(
            type='data',
            array=df_global['bpm_std']
        )
    ))
    
    fig.update_layout(
        title='BPM Médio - Praticantes vs Não Praticantes',
        xaxis_title='Grupo',
        yaxis_title='BPM Médio',
        template='plotly_white',
        showlegend=False,
        height=500
    )
    
    return fig


def plot_bpm_by_age_heatmap(
    df_by_age: pd.DataFrame,
    save_path: Optional[Path] = None
) -> go.Figure:
    """
    Heatmap de BPM médio segmentado por idade e grupo.
    """
    # Pivotar dados
    df_pivot = df_by_age.pivot(
        index='faixa_idade',
        columns='grupo',
        values='bpm_mean'
    )
    
    fig = go.Figure(data=go.Heatmap(
        z=df_pivot.values,
        x=df_pivot.columns,
        y=df_pivot.index,
        colorscale='RdYlBu_r',
        text=df_pivot.values.round(1),
        texttemplate='%{text}',
        textfont={"size": 12},
        colorbar=dict(title="BPM Médio")
    ))
    
    fig.update_layout(
        title='BPM Médio por Faixa de Idade e Grupo',
        xaxis_title='Grupo',
        yaxis_title='Faixa de Idade',
        template='plotly_white',
        height=500
    )
    
    if save_path:
        fig.write_html(save_path)
    
    return fig


def plot_bpm_practitioners_static(
    df_global: pd.DataFrame,
    df_by_age: pd.DataFrame,
    save_path: Optional[Path] = None
):
    """
    Versão estática do plot de BPM praticantes (PNG).
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Comparação global
    colors = ['#f39c12', '#34495e']
    axes[0].bar(df_global['grupo'], df_global['bpm_mean'], color=colors)
    axes[0].errorbar(df_global['grupo'], df_global['bpm_mean'], yerr=df_global['bpm_std'], 
                     fmt='none', ecolor='black', capsize=5)
    axes[0].set_title('BPM Médio - Comparação Global')
    axes[0].set_ylabel('BPM Médio')
    axes[0].tick_params(axis='x', rotation=45)
    
    # Por faixa de idade
    df_pivot = df_by_age.pivot(index='faixa_idade', columns='grupo', values='bpm_mean')
    df_pivot.plot(kind='bar', ax=axes[1], color=['#f39c12', '#34495e'])
    axes[1].set_title('BPM Médio por Faixa de Idade')
    axes[1].set_xlabel('Faixa de Idade')
    axes[1].set_ylabel('BPM Médio')
    axes[1].legend(title='Grupo')
    axes[1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        return fig


# =============================================================================
# FUNÇÃO PRINCIPAL PARA BATCH
# =============================================================================

def main():
    """
    Gera todos os gráficos em batch mode.
    
    Uso: python -m src.plots_v2
    """
    from src.analysis_v2 import (
        analyze_smokers_vs_nonsmokers,
        analyze_runners_vs_nonrunners,
        analyze_practice_by_age,
        analyze_bpm_practitioners_vs_nonpractitioners
    )
    
    print("=" * 80)
    print("GERANDO VISUALIZAÇÕES - BATCH MODE")
    print("=" * 80)
    
    # Carregar dados
    print("\nCarregando dataset...")
    data_path = Path("data/external/fitlife_clean.csv")
    df = pd.read_csv(data_path)
    print(f"Dataset carregado: {len(df):,} linhas")
    
    # Criar diretórios
    Path("reports/figs_interactive").mkdir(parents=True, exist_ok=True)
    Path("reports/figs_static").mkdir(parents=True, exist_ok=True)
    
    print("\n" + "=" * 80)
    print("Análise 1: Fumantes vs Não Fumantes")
    print("=" * 80)
    
    # Plotly
    plot_smokers_comparison_boxplot(df, 'bpm', Path("reports/figs_interactive/analise1_bpm_boxplot.html"))
    plot_smokers_comparison_boxplot(df, 'calorias_kcal', Path("reports/figs_interactive/analise1_calorias_boxplot.html"))
    plot_smokers_comparison_violin(df, 'bpm', Path("reports/figs_interactive/analise1_bpm_violin.html"))
    
    # Static
    plot_smokers_comparison_static(df, Path("reports/figs_static/analise1_comparacao.png"))
    
    print("  Gerados: 4 gráficos")
    
    print("\n" + "=" * 80)
    print("Análise 2: Runners vs Não Runners")
    print("=" * 80)
    
    # Plotly
    plot_runners_comparison_boxplot(df, 'bpm', Path("reports/figs_interactive/analise2_bpm_boxplot.html"))
    plot_runners_comparison_boxplot(df, 'calorias_kcal', Path("reports/figs_interactive/analise2_calorias_boxplot.html"))
    plot_runners_comparison_histogram(df, 'calorias_kcal', Path("reports/figs_interactive/analise2_calorias_hist.html"))
    
    # Static
    plot_runners_comparison_static(df, Path("reports/figs_static/analise2_comparacao.png"))
    
    print("  Gerados: 4 gráficos")
    
    print("\n" + "=" * 80)
    print("Análise 3: Prática por Faixa de Idade")
    print("=" * 80)
    
    df_age, _ = analyze_practice_by_age(df)
    
    # Plotly
    plot_practice_by_age_bars(df_age, Path("reports/figs_interactive/analise3_taxa_barras.html"))
    plot_practice_by_age_stacked(df_age, Path("reports/figs_interactive/analise3_stacked.html"))
    
    # Static
    plot_practice_by_age_static(df_age, Path("reports/figs_static/analise3_idade.png"))
    
    print("  Gerados: 3 gráficos")
    
    print("\n" + "=" * 80)
    print("Análise 4: BPM Praticantes vs Não Praticantes")
    print("=" * 80)
    
    df_bpm_global, df_bpm_age, _ = analyze_bpm_practitioners_vs_nonpractitioners(df)
    
    # Plotly
    plot_bpm_practitioners_comparison(df_bpm_global, Path("reports/figs_interactive/analise4_comparacao.html"))
    plot_bpm_by_age_heatmap(df_bpm_age, Path("reports/figs_interactive/analise4_heatmap.html"))
    
    # Static
    plot_bpm_practitioners_static(df_bpm_global, df_bpm_age, Path("reports/figs_static/analise4_bpm.png"))
    
    print("  Gerados: 3 gráficos")
    
    print("\n" + "=" * 80)
    print("✅ VISUALIZAÇÕES CONCLUÍDAS!")
    print(f"   Interativos (HTML): reports/figs_interactive/")
    print(f"   Estáticos (PNG): reports/figs_static/")
    print("=" * 80)


if __name__ == "__main__":
    main()

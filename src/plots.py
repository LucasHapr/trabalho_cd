"""
Módulo de visualizações.

Este módulo implementa funções para criar gráficos interativos (Plotly)
e estáticos (Seaborn/Matplotlib) para as 4 análises principais.
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
from plotly.subplots import make_subplots


# Configurações padrão
PLOTLY_TEMPLATE = "plotly_white"
SEABORN_STYLE = "whitegrid"
FIGURE_DPI = 300
COLOR_PALETTE = px.colors.qualitative.Set2


def setup_plotting_style():
    """Configura estilos padrão para os gráficos."""
    sns.set_style(SEABORN_STYLE)
    plt.rcParams["figure.dpi"] = FIGURE_DPI
    plt.rcParams["savefig.dpi"] = FIGURE_DPI
    plt.rcParams["font.size"] = 10


def save_plotly_fig(fig, filepath: Union[str, Path], formats: List[str] = ["html"]):
    """
    Salva figura Plotly em múltiplos formatos.

    Args:
        fig: Figura Plotly
        filepath: Caminho base (sem extensão)
        formats: Lista de formatos ('html', 'png', 'jpg', 'svg')
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    for fmt in formats:
        output_path = filepath.with_suffix(f".{fmt}")
        if fmt == "html":
            fig.write_html(output_path)
            print(f"  💾 Salvo: {output_path}")
        else:
            try:
                fig.write_image(output_path)
                print(f"  💾 Salvo: {output_path}")
            except Exception as e:
                print(f"  ⚠️  Erro ao salvar {fmt}: {e}")


def save_matplotlib_fig(fig, filepath: Union[str, Path], formats: List[str] = ["png"]):
    """
    Salva figura Matplotlib em múltiplos formatos.

    Args:
        fig: Figura Matplotlib
        filepath: Caminho base (sem extensão)
        formats: Lista de formatos ('png', 'jpg', 'svg', 'pdf')
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    for fmt in formats:
        output_path = filepath.with_suffix(f".{fmt}")
        fig.savefig(output_path, dpi=FIGURE_DPI, bbox_inches="tight")
        print(f"  💾 Salvo: {output_path}")


# ============================================================================
# ANÁLISE 1: Fumantes vs Não Fumantes
# ============================================================================


def plot_smokers_comparison_boxplot_plotly(df: pd.DataFrame, metric: str = "pace_min_km") -> go.Figure:
    """
    Boxplot comparando fumantes vs não fumantes (Plotly).

    Args:
        df: DataFrame com atividades esportivas
        metric: Métrica a comparar

    Returns:
        Figura Plotly
    """
    df_plot = df[df[metric].notna()].copy()
    df_plot["Status"] = df_plot["is_smoker"].map({True: "Fumante", False: "Não Fumante"})

    fig = px.box(
        df_plot,
        x="Status",
        y=metric,
        color="Status",
        title=f"Comparação de {metric} entre Fumantes e Não Fumantes",
        labels={metric: metric.replace("_", " ").title()},
        template=PLOTLY_TEMPLATE,
        color_discrete_sequence=COLOR_PALETTE,
    )

    fig.update_layout(showlegend=False, height=500)

    return fig


def plot_smokers_comparison_boxplot_seaborn(
    df: pd.DataFrame, metric: str = "pace_min_km"
) -> plt.Figure:
    """
    Boxplot comparando fumantes vs não fumantes (Seaborn).

    Args:
        df: DataFrame com atividades esportivas
        metric: Métrica a comparar

    Returns:
        Figura Matplotlib
    """
    df_plot = df[df[metric].notna()].copy()
    df_plot["Status"] = df_plot["is_smoker"].map({True: "Fumante", False: "Não Fumante"})

    fig, ax = plt.subplots(figsize=(10, 6))

    sns.boxplot(data=df_plot, x="Status", y=metric, palette="Set2", ax=ax)

    ax.set_title(f"Comparação de {metric} entre Fumantes e Não Fumantes", fontsize=14, fontweight="bold")
    ax.set_xlabel("Status de Fumante", fontsize=12)
    ax.set_ylabel(metric.replace("_", " ").title(), fontsize=12)

    plt.tight_layout()
    return fig


def plot_smokers_comparison_bars_plotly(df_summary: pd.DataFrame, metric: str = "bpm") -> go.Figure:
    """
    Gráfico de barras com erro comparando fumantes vs não fumantes (Plotly).

    Args:
        df_summary: DataFrame com estatísticas agregadas
        metric: Métrica a comparar

    Returns:
        Figura Plotly
    """
    mean_col = f"{metric}_mean"
    std_col = f"{metric}_std"

    if mean_col not in df_summary.columns:
        print(f"⚠️  Coluna {mean_col} não encontrada")
        return go.Figure()

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df_summary["grupo"],
            y=df_summary[mean_col],
            error_y=dict(type="data", array=df_summary[std_col]) if std_col in df_summary.columns else None,
            marker_color=COLOR_PALETTE[:len(df_summary)],
            text=df_summary[mean_col].round(2),
            textposition="outside",
        )
    )

    fig.update_layout(
        title=f"Comparação de {metric} (Média ± DP)",
        xaxis_title="Grupo",
        yaxis_title=metric.replace("_", " ").title(),
        template=PLOTLY_TEMPLATE,
        showlegend=False,
        height=500,
    )

    return fig


# ============================================================================
# ANÁLISE 2: Runners vs Não Runners
# ============================================================================


def plot_runners_comparison_violin_plotly(df: pd.DataFrame, metric: str = "pace_min_km") -> go.Figure:
    """
    Violin plot comparando runners vs não runners (Plotly).

    Args:
        df: DataFrame processado
        metric: Métrica a comparar

    Returns:
        Figura Plotly
    """
    df_plot = df[df[metric].notna()].copy()
    df_plot["Status"] = df_plot["is_runner"].map({True: "Runner", False: "Não Runner"})

    fig = px.violin(
        df_plot,
        x="Status",
        y=metric,
        color="Status",
        box=True,
        title=f"Distribuição de {metric}: Runners vs Não Runners",
        labels={metric: metric.replace("_", " ").title()},
        template=PLOTLY_TEMPLATE,
        color_discrete_sequence=COLOR_PALETTE,
    )

    fig.update_layout(showlegend=False, height=500)

    return fig


def plot_runners_comparison_ecdf_plotly(df: pd.DataFrame, metric: str = "pace_min_km") -> go.Figure:
    """
    ECDF comparando runners vs não runners (Plotly).

    Args:
        df: DataFrame processado
        metric: Métrica a comparar

    Returns:
        Figura Plotly
    """
    df_plot = df[df[metric].notna()].copy()
    df_plot["Status"] = df_plot["is_runner"].map({True: "Runner", False: "Não Runner"})

    fig = px.ecdf(
        df_plot,
        x=metric,
        color="Status",
        title=f"Função de Distribuição Acumulada: {metric}",
        labels={metric: metric.replace("_", " ").title(), "Status": "Grupo"},
        template=PLOTLY_TEMPLATE,
        color_discrete_sequence=COLOR_PALETTE,
    )

    fig.update_layout(height=500)

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

    fig.add_trace(
        go.Bar(
            x=df_rates["faixa_idade"],
            y=df_rates["taxa_praticantes_pct"],
            marker_color=COLOR_PALETTE[0],
            text=df_rates["taxa_praticantes_pct"].round(1).astype(str) + "%",
            textposition="outside",
        )
    )

    fig.update_layout(
        title="Taxa de Praticantes de Atividades Físicas por Faixa de Idade",
        xaxis_title="Faixa de Idade",
        yaxis_title="Taxa de Praticantes (%)",
        template=PLOTLY_TEMPLATE,
        showlegend=False,
        height=500,
    )

    return fig


def plot_practice_by_age_stacked_plotly(df_rates: pd.DataFrame) -> go.Figure:
    """
    Gráfico de barras empilhadas com praticantes vs não praticantes (Plotly).

    Args:
        df_rates: DataFrame com taxas por faixa de idade

    Returns:
        Figura Plotly
    """
    df_plot = df_rates.copy()
    df_plot["nao_praticantes"] = df_plot["total"] - df_plot["praticantes"]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            name="Praticantes",
            x=df_plot["faixa_idade"],
            y=df_plot["praticantes"],
            marker_color=COLOR_PALETTE[0],
        )
    )

    fig.add_trace(
        go.Bar(
            name="Não Praticantes",
            x=df_plot["faixa_idade"],
            y=df_plot["nao_praticantes"],
            marker_color=COLOR_PALETTE[1],
        )
    )

    fig.update_layout(
        title="Distribuição de Praticantes e Não Praticantes por Faixa de Idade",
        xaxis_title="Faixa de Idade",
        yaxis_title="Número de Pessoas",
        barmode="stack",
        template=PLOTLY_TEMPLATE,
        height=500,
    )

    return fig


def plot_practice_by_age_metrics_seaborn(df_metrics: pd.DataFrame) -> plt.Figure:
    """
    Gráfico de métricas médias por faixa de idade (Seaborn).

    Args:
        df_metrics: DataFrame com métricas por faixa de idade

    Returns:
        Figura Matplotlib
    """
    # Selecionar colunas de média
    mean_cols = [col for col in df_metrics.columns if "_mean" in col]

    if len(mean_cols) == 0:
        print("⚠️  Nenhuma coluna de média encontrada")
        return plt.figure()

    n_metrics = len(mean_cols)
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()

    for idx, col in enumerate(mean_cols[:4]):  # Limitar a 4 métricas
        metric_name = col.replace("_mean", "").replace("_", " ").title()

        axes[idx].bar(df_metrics["faixa_idade"], df_metrics[col], color=COLOR_PALETTE[idx % len(COLOR_PALETTE)])
        axes[idx].set_title(f"{metric_name} Médio por Idade", fontsize=12, fontweight="bold")
        axes[idx].set_xlabel("Faixa de Idade", fontsize=10)
        axes[idx].set_ylabel(metric_name, fontsize=10)
        axes[idx].tick_params(axis="x", rotation=45)

    # Remover eixos extras
    for idx in range(n_metrics, len(axes)):
        fig.delaxes(axes[idx])

    plt.tight_layout()
    return fig


# ============================================================================
# ANÁLISE 4: BPM Praticantes vs Não Praticantes
# ============================================================================


def plot_bpm_comparison_bars_plotly(df_summary: pd.DataFrame) -> go.Figure:
    """
    Gráfico de barras comparando BPM de praticantes vs não praticantes (Plotly).

    Args:
        df_summary: DataFrame com estatísticas de BPM

    Returns:
        Figura Plotly
    """
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df_summary["grupo"],
            y=df_summary["bpm_mean"],
            error_y=dict(type="data", array=df_summary["bpm_std"]),
            marker_color=COLOR_PALETTE[:len(df_summary)],
            text=df_summary["bpm_mean"].round(1),
            textposition="outside",
        )
    )

    fig.update_layout(
        title="BPM Médio: Praticantes vs Não Praticantes",
        xaxis_title="Grupo",
        yaxis_title="BPM Médio",
        template=PLOTLY_TEMPLATE,
        showlegend=False,
        height=500,
    )

    return fig


def plot_bpm_by_age_heatmap_plotly(df_by_age: pd.DataFrame) -> go.Figure:
    """
    Heatmap de BPM por faixa de idade e status de praticante (Plotly).

    Args:
        df_by_age: DataFrame com BPM por idade e status

    Returns:
        Figura Plotly
    """
    # Pivot dos dados
    df_pivot = df_by_age.pivot(index="faixa_idade", columns="grupo", values="mean")

    fig = go.Figure(
        data=go.Heatmap(
            z=df_pivot.values,
            x=df_pivot.columns,
            y=df_pivot.index,
            colorscale="RdYlBu_r",
            text=df_pivot.values.round(1),
            texttemplate="%{text}",
            textfont={"size": 12},
        )
    )

    fig.update_layout(
        title="Heatmap de BPM Médio por Faixa de Idade e Status",
        xaxis_title="Status",
        yaxis_title="Faixa de Idade",
        template=PLOTLY_TEMPLATE,
        height=500,
    )

    return fig


def plot_bpm_by_age_grouped_seaborn(df_by_age: pd.DataFrame) -> plt.Figure:
    """
    Gráfico de barras agrupadas de BPM por idade e status (Seaborn).

    Args:
        df_by_age: DataFrame com BPM por idade e status

    Returns:
        Figura Matplotlib
    """
    fig, ax = plt.subplots(figsize=(12, 6))

    # Criar coluna 'grupo' se não existir
    if "grupo" not in df_by_age.columns and "is_practitioner" in df_by_age.columns:
        df_by_age = df_by_age.copy()
        df_by_age["grupo"] = df_by_age["is_practitioner"].map(
            {True: "Praticante", False: "Não Praticante"}
        )

    sns.barplot(data=df_by_age, x="faixa_idade", y="mean", hue="grupo", palette="Set2", ax=ax)

    ax.set_title("BPM Médio por Faixa de Idade e Status", fontsize=14, fontweight="bold")
    ax.set_xlabel("Faixa de Idade", fontsize=12)
    ax.set_ylabel("BPM Médio", fontsize=12)
    ax.legend(title="Status")

    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig


# ============================================================================
# Função auxiliar para gerar todos os gráficos
# ============================================================================


def generate_all_plots(
    df: pd.DataFrame,
    results: Dict,
    output_dir: Union[str, Path] = "reports",
    save_interactive: bool = True,
    save_static: bool = True,
) -> Dict[str, Dict[str, go.Figure]]:
    """
    Gera todos os gráficos das 4 análises.

    Args:
        df: DataFrame processado
        results: Dicionário com resultados das análises
        output_dir: Diretório de saída
        save_interactive: Se True, salva versões interativas (HTML)
        save_static: Se True, salva versões estáticas (PNG)

    Returns:
        Dicionário com todas as figuras geradas
    """
    print("\n🎨 Gerando visualizações...")

    setup_plotting_style()

    output_dir = Path(output_dir)
    interactive_dir = output_dir / "figs_interactive"
    static_dir = output_dir / "figs_static"

    all_figs = {}

    # Análise 1: Fumantes vs Não Fumantes
    print("\n  📊 Análise 1: Fumantes vs Não Fumantes")
    all_figs["smokers"] = {}

    # Filtrar dados para esporte
    sport_activities = ["Running", "Walking", "Cycling", "Swimming", "Jogging", "Hiking"]
    pattern = "|".join(sport_activities)
    df_sports = df[df["atividade"].str.contains(pattern, case=False, na=False)]

    # Boxplot pace
    fig = plot_smokers_comparison_boxplot_plotly(df_sports, "pace_min_km")
    all_figs["smokers"]["boxplot_pace_plotly"] = fig
    if save_interactive:
        save_plotly_fig(fig, interactive_dir / "smokers_boxplot_pace")

    fig = plot_smokers_comparison_boxplot_seaborn(df_sports, "pace_min_km")
    all_figs["smokers"]["boxplot_pace_seaborn"] = fig
    if save_static:
        save_matplotlib_fig(fig, static_dir / "smokers_boxplot_pace")
    plt.close(fig)

    # Barras BPM
    if "smokers_vs_nonsmokers" in results and "summary" in results["smokers_vs_nonsmokers"]:
        df_summary = results["smokers_vs_nonsmokers"]["summary"]
        fig = plot_smokers_comparison_bars_plotly(df_summary, "bpm")
        all_figs["smokers"]["bars_bpm"] = fig
        if save_interactive:
            save_plotly_fig(fig, interactive_dir / "smokers_bars_bpm")

    # Análise 2: Runners vs Não Runners
    print("\n  📊 Análise 2: Runners vs Não Runners")
    all_figs["runners"] = {}

    # Violin plot
    fig = plot_runners_comparison_violin_plotly(df, "pace_min_km")
    all_figs["runners"]["violin_pace"] = fig
    if save_interactive:
        save_plotly_fig(fig, interactive_dir / "runners_violin_pace")

    # ECDF
    fig = plot_runners_comparison_ecdf_plotly(df, "pace_min_km")
    all_figs["runners"]["ecdf_pace"] = fig
    if save_interactive:
        save_plotly_fig(fig, interactive_dir / "runners_ecdf_pace")

    # Histogram
    fig = plot_runners_comparison_histogram_seaborn(df, "pace_min_km")
    all_figs["runners"]["histogram_pace"] = fig
    if save_static:
        save_matplotlib_fig(fig, static_dir / "runners_histogram_pace")
    plt.close(fig)

    # Análise 3: Prática por Idade
    print("\n  📊 Análise 3: Prática por Idade")
    all_figs["age"] = {}

    if "practice_by_age" in results:
        df_rates = results["practice_by_age"]["rates"]
        df_metrics = results["practice_by_age"]["metrics"]

        # Barras taxa
        fig = plot_practice_by_age_bars_plotly(df_rates)
        all_figs["age"]["bars_rate"] = fig
        if save_interactive:
            save_plotly_fig(fig, interactive_dir / "age_bars_rate")

        # Barras empilhadas
        fig = plot_practice_by_age_stacked_plotly(df_rates)
        all_figs["age"]["stacked"] = fig
        if save_interactive:
            save_plotly_fig(fig, interactive_dir / "age_stacked")

        # Métricas
        if not df_metrics.empty:
            fig = plot_practice_by_age_metrics_seaborn(df_metrics)
            all_figs["age"]["metrics"] = fig
            if save_static:
                save_matplotlib_fig(fig, static_dir / "age_metrics")
            plt.close(fig)

    # Análise 4: BPM Praticantes
    print("\n  📊 Análise 4: BPM Praticantes")
    all_figs["bpm"] = {}

    if "bpm_practitioners" in results:
        df_summary = results["bpm_practitioners"]["summary"]
        stats_dict = results["bpm_practitioners"]["stats"]

        # Barras
        fig = plot_bpm_comparison_bars_plotly(df_summary)
        all_figs["bpm"]["bars"] = fig
        if save_interactive:
            save_plotly_fig(fig, interactive_dir / "bpm_bars")

        # Heatmap por idade
        if "by_age" in stats_dict:
            df_by_age = stats_dict["by_age"]
            fig = plot_bpm_by_age_heatmap_plotly(df_by_age)
            all_figs["bpm"]["heatmap"] = fig
            if save_interactive:
                save_plotly_fig(fig, interactive_dir / "bpm_heatmap")

            fig = plot_bpm_by_age_grouped_seaborn(df_by_age)
            all_figs["bpm"]["grouped"] = fig
            if save_static:
                save_matplotlib_fig(fig, static_dir / "bpm_grouped")
            plt.close(fig)

    print("\n✅ Visualizações geradas com sucesso!")
    return all_figs


if __name__ == "__main__":
    setup_plotting_style()
    print("✓ Módulo plots carregado com sucesso")

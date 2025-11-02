"""
Aplicação Streamlit - Dashboard de Análise de Fitness e Saúde

Este dashboard apresenta análises interativas sobre os dados de fitness,
incluindo comparações entre fumantes, praticantes de corrida, faixas de idade e BPM.
"""

import sys
from pathlib import Path

import pandas as pd
import streamlit as st
from hydra import compose, initialize_config_dir

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.analysis import (
    analyze_bpm_practitioners_vs_nonpractitioners,
    analyze_practice_by_age,
    analyze_runners_vs_nonrunners,
    analyze_smokers_vs_nonsmokers,
)
from src.dataio import load_data
from src.plots import (
    plot_bpm_by_age_heatmap_plotly,
    plot_bpm_comparison_bars_plotly,
    plot_practice_by_age_bars_plotly,
    plot_practice_by_age_stacked_plotly,
    plot_runners_comparison_ecdf_plotly,
    plot_runners_comparison_violin_plotly,
    plot_smokers_comparison_bars_plotly,
    plot_smokers_comparison_boxplot_plotly,
)
from src.preprocess import preprocess_pipeline

# Configuração da página
st.set_page_config(
    page_title="Dashboard Fitness & Saúde",
    page_icon="🏃",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def load_and_process_data(use_public: bool, use_wearable: bool):
    """
    Carrega e processa os dados (com cache).

    Args:
        use_public: Se True, carrega dataset público
        use_wearable: Se True, carrega dataset wearable

    Returns:
        DataFrame processado
    """
    # Inicializar Hydra
    config_dir = Path(__file__).parent / "conf"

    with initialize_config_dir(config_dir=str(config_dir.absolute()), version_base=None):
        cfg = compose(config_name="config", overrides=[f"use_public={use_public}", f"use_wearable={use_wearable}"])

    # Carregar dados
    df_public = None
    df_wearable = None

    if use_public:
        try:
            public_path = Path(cfg.external.path)
            if public_path.exists():
                df_public = load_data(public_path)
                st.sidebar.success(f"✅ Dataset público carregado: {len(df_public)} linhas")
            else:
                st.sidebar.warning(f"⚠️ Dataset público não encontrado: {public_path}")
        except Exception as e:
            st.sidebar.error(f"❌ Erro ao carregar dataset público: {e}")

    if use_wearable:
        try:
            wearable_path = Path(cfg.wearable.path)
            if wearable_path.exists():
                df_wearable = load_data(wearable_path)
                st.sidebar.success(f"✅ Dataset wearable carregado: {len(df_wearable)} linhas")
            else:
                st.sidebar.warning(f"⚠️ Dataset wearable não encontrado: {wearable_path}")
        except Exception as e:
            st.sidebar.error(f"❌ Erro ao carregar dataset wearable: {e}")

    # Processar
    if df_public is None and df_wearable is None:
        st.error("❌ Nenhum dataset foi carregado. Verifique os caminhos na configuração.")
        return None

    df_processed = preprocess_pipeline(df_public, df_wearable, cfg, validate=False)

    return df_processed


def apply_sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica filtros da sidebar ao DataFrame.

    Args:
        df: DataFrame processado

    Returns:
        DataFrame filtrado
    """
    st.sidebar.header("🔍 Filtros")

    # Filtro de faixa de idade
    if "faixa_idade" in df.columns:
        faixas = df["faixa_idade"].dropna().unique()
        selected_faixas = st.sidebar.multiselect(
            "Faixa de Idade", options=sorted(faixas), default=sorted(faixas)
        )
        if selected_faixas:
            df = df[df["faixa_idade"].isin(selected_faixas)]

    # Filtro de status de fumante
    if "is_smoker" in df.columns:
        smoker_filter = st.sidebar.radio(
            "Status de Fumante", options=["Todos", "Fumante", "Não Fumante"], index=0
        )
        if smoker_filter == "Fumante":
            df = df[df["is_smoker"]]
        elif smoker_filter == "Não Fumante":
            df = df[~df["is_smoker"]]

    # Filtro de praticante
    if "is_practitioner" in df.columns:
        pract_filter = st.sidebar.radio(
            "Status de Praticante", options=["Todos", "Praticante", "Não Praticante"], index=0
        )
        if pract_filter == "Praticante":
            df = df[df["is_practitioner"]]
        elif pract_filter == "Não Praticante":
            df = df[~df["is_practitioner"]]

    # Filtro de período
    if "dt" in df.columns:
        min_date = df["dt"].min().date()
        max_date = df["dt"].max().date()

        date_range = st.sidebar.date_input(
            "Período",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
        )

        if len(date_range) == 2:
            start_date, end_date = date_range
            df = df[(df["dt"].dt.date >= start_date) & (df["dt"].dt.date <= end_date)]

    return df


def show_kpis(df: pd.DataFrame):
    """
    Mostra KPIs principais no topo do dashboard.

    Args:
        df: DataFrame processado
    """
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("📊 Total de Registros", f"{len(df):,}")

    with col2:
        if "bpm" in df.columns:
            bpm_mean = df["bpm"].mean()
            st.metric("💓 BPM Médio", f"{bpm_mean:.1f}")

    with col3:
        if "pace_min_km" in df.columns:
            pace_mean = df["pace_min_km"].dropna().mean()
            st.metric("⏱️ Pace Médio", f"{pace_mean:.2f} min/km")

    with col4:
        if "is_smoker" in df.columns:
            smoker_pct = df["is_smoker"].mean() * 100
            st.metric("🚬 % Fumantes", f"{smoker_pct:.1f}%")

    with col5:
        if "is_practitioner" in df.columns:
            pract_pct = df["is_practitioner"].mean() * 100
            st.metric("🏃 % Praticantes", f"{pract_pct:.1f}%")


def show_analysis_1(df: pd.DataFrame):
    """
    Análise 1: Fumantes vs Não Fumantes em Esportes.

    Args:
        df: DataFrame processado
    """
    st.header("📊 Análise 1: Fumantes vs Não Fumantes em Esportes")

    st.markdown(
        """
    Esta análise compara o desempenho em atividades esportivas entre fumantes e não fumantes,
    avaliando métricas como pace, BPM, calorias e passos.
    """
    )

    # Filtrar atividades esportivas
    sport_activities = ["Running", "Walking", "Cycling", "Swimming", "Jogging", "Hiking"]
    pattern = "|".join(sport_activities)
    df_sports = df[df["atividade"].str.contains(pattern, case=False, na=False)]

    if len(df_sports) == 0:
        st.warning("⚠️ Nenhuma atividade esportiva encontrada nos dados filtrados.")
        return

    # Análise
    df_summary, stats_dict = analyze_smokers_vs_nonsmokers(df_sports, sport_activities)

    # Mostrar tabela resumo
    st.subheader("📋 Resumo Estatístico")
    st.dataframe(df_summary, use_container_width=True)

    # Gráficos
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Pace (min/km)")
        if "pace_min_km" in df_sports.columns:
            fig = plot_smokers_comparison_boxplot_plotly(df_sports, "pace_min_km")
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("BPM Médio")
        if "bpm_mean" in df_summary.columns:
            fig = plot_smokers_comparison_bars_plotly(df_summary, "bpm")
            st.plotly_chart(fig, use_container_width=True)

    # Testes estatísticos
    if stats_dict:
        st.subheader("🧪 Testes Estatísticos (Mann-Whitney U)")
        stats_df = pd.DataFrame(stats_dict).T
        stats_df["significant"] = stats_df["significant"].map({True: "✅ Sim", False: "❌ Não"})
        st.dataframe(stats_df, use_container_width=True)


def show_analysis_2(df: pd.DataFrame):
    """
    Análise 2: Praticantes vs Não Praticantes de Corrida.

    Args:
        df: DataFrame processado
    """
    st.header("📊 Análise 2: Praticantes vs Não Praticantes de Corrida (Pace)")

    st.markdown(
        """
    Esta análise compara o pace (ritmo) e outras métricas entre quem pratica corrida
    e quem não pratica, investigando diferenças de performance.
    """
    )

    # Análise
    df_summary, stats_dict = analyze_runners_vs_nonrunners(df)

    if df_summary.empty:
        st.warning("⚠️ Dados insuficientes para análise de runners.")
        return

    # Mostrar tabela resumo
    st.subheader("📋 Resumo Estatístico")
    st.dataframe(df_summary, use_container_width=True)

    # Gráficos
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Distribuição de Pace (Violin Plot)")
        if "pace_min_km" in df.columns:
            fig = plot_runners_comparison_violin_plotly(df, "pace_min_km")
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Função de Distribuição Acumulada (ECDF)")
        if "pace_min_km" in df.columns:
            fig = plot_runners_comparison_ecdf_plotly(df, "pace_min_km")
            st.plotly_chart(fig, use_container_width=True)

    # Testes estatísticos
    if stats_dict:
        st.subheader("🧪 Testes Estatísticos (Mann-Whitney U)")
        stats_df = pd.DataFrame(stats_dict).T
        stats_df["significant"] = stats_df["significant"].map({True: "✅ Sim", False: "❌ Não"})
        st.dataframe(stats_df, use_container_width=True)


def show_analysis_3(df: pd.DataFrame):
    """
    Análise 3: Prática de Esportes por Faixas de Idade.

    Args:
        df: DataFrame processado
    """
    st.header("📊 Análise 3: Prática de Esportes por Faixas de Idade")

    st.markdown(
        """
    Esta análise investiga como a prática de atividades físicas varia entre diferentes
    faixas etárias, incluindo taxas de participação e métricas médias.
    """
    )

    # Análise
    df_rates, df_metrics = analyze_practice_by_age(df)

    if df_rates.empty:
        st.warning("⚠️ Dados insuficientes para análise por idade.")
        return

    # Mostrar tabela de taxas
    st.subheader("📋 Taxa de Praticantes por Faixa de Idade")
    st.dataframe(df_rates, use_container_width=True)

    # Gráficos
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Taxa de Praticantes (%)")
        fig = plot_practice_by_age_bars_plotly(df_rates)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Distribuição: Praticantes vs Não Praticantes")
        fig = plot_practice_by_age_stacked_plotly(df_rates)
        st.plotly_chart(fig, use_container_width=True)

    # Métricas médias
    if not df_metrics.empty:
        st.subheader("📊 Métricas Médias por Faixa de Idade (Apenas Praticantes)")
        st.dataframe(df_metrics, use_container_width=True)


def show_analysis_4(df: pd.DataFrame):
    """
    Análise 4: BPM Praticantes vs Não Praticantes.

    Args:
        df: DataFrame processado
    """
    st.header("📊 Análise 4: Comparação de BPM entre Praticantes e Não Praticantes")

    st.markdown(
        """
    Esta análise compara o BPM médio entre quem pratica atividades físicas e quem não pratica,
    incluindo análise estratificada por faixa etária.
    """
    )

    # Análise
    df_summary, stats_dict = analyze_bpm_practitioners_vs_nonpractitioners(df)

    if df_summary.empty:
        st.warning("⚠️ Dados insuficientes para análise de BPM.")
        return

    # Mostrar tabela resumo
    st.subheader("📋 Resumo Estatístico Geral")
    st.dataframe(df_summary, use_container_width=True)

    # Gráficos
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("BPM Médio por Grupo")
        fig = plot_bpm_comparison_bars_plotly(df_summary)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Heatmap: BPM por Idade e Status")
        if "by_age" in stats_dict:
            df_by_age = stats_dict["by_age"]
            fig = plot_bpm_by_age_heatmap_plotly(df_by_age)
            st.plotly_chart(fig, use_container_width=True)

    # Teste estatístico
    if "overall" in stats_dict:
        st.subheader("🧪 Teste Estatístico (Mann-Whitney U)")
        result = stats_dict["overall"]
        col1, col2, col3 = st.columns(3)
        col1.metric("Estatística", f"{result['statistic']:.2f}")
        col2.metric("P-valor", f"{result['pvalue']:.4f}")
        col3.metric("Significativo", "✅ Sim" if result["significant"] else "❌ Não")


def main():
    """Função principal do aplicativo Streamlit."""
    # Título
    st.title("🏃 Dashboard de Análise de Fitness e Saúde")

    st.markdown(
        """
    Este dashboard apresenta análises interativas sobre dados de fitness e saúde,
    comparando métricas entre diferentes grupos e faixas etárias.
    """
    )

    # Sidebar - Seleção de datasets
    st.sidebar.title("⚙️ Configurações")

    use_public = st.sidebar.checkbox("Usar Dataset Público", value=False)
    use_wearable = st.sidebar.checkbox("Usar Dataset Wearable (JSON)", value=True)

    if not use_public and not use_wearable:
        st.warning("⚠️ Selecione pelo menos um dataset na sidebar.")
        return

    # Carregar dados
    with st.spinner("Carregando e processando dados..."):
        df = load_and_process_data(use_public, use_wearable)

    if df is None or len(df) == 0:
        st.error("❌ Nenhum dado foi carregado. Verifique os caminhos dos arquivos.")
        return

    # Aplicar filtros
    df_filtered = apply_sidebar_filters(df)

    st.sidebar.markdown(f"**Registros após filtros:** {len(df_filtered):,}")

    # Mostrar KPIs
    show_kpis(df_filtered)

    st.markdown("---")

    # Abas de análise
    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "🚬 Fumantes vs Não Fumantes",
            "🏃 Runners vs Não Runners",
            "📅 Prática por Idade",
            "💓 BPM Praticantes",
        ]
    )

    with tab1:
        show_analysis_1(df_filtered)

    with tab2:
        show_analysis_2(df_filtered)

    with tab3:
        show_analysis_3(df_filtered)

    with tab4:
        show_analysis_4(df_filtered)

    # Rodapé
    st.markdown("---")
    st.markdown(
        """
    <div style='text-align: center'>
        <p>📊 Dashboard desenvolvido com Streamlit | 🐍 Python + Plotly + Pandas</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()

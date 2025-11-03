"""
Dashboard Streamlit para Análise de Fitness e Saúde - Versão 2
Otimizado para dataset fitlife_clean.csv

4 abas de análise:
1. Fumantes vs Não Fumantes
2. Runners vs Não Runners
3. Prática por Faixa de Idade
4. BPM Praticantes vs Não Praticantes

Com filtros na sidebar: faixa de idade, fumante/não, período
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
from src.plots import (
    plot_bpm_by_age_heatmap,
    plot_bpm_practitioners_comparison,
    plot_practice_by_age_bars,
    plot_practice_by_age_bars_plotly,
    plot_practice_by_age_stacked,
    plot_runners_comparison_boxplot,
    plot_runners_comparison_histogram,
    plot_smokers_comparison_boxplot,
    plot_smokers_comparison_violin,
)
from src.preprocess import preprocess_pipeline

# Configuração da página
st.set_page_config(
    page_title="Dashboard Fitness & Saúde",
    page_icon="📊",
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
                df_public = pd.read_csv(public_path)
            else:
                st.sidebar.warning(f"Dataset público não encontrado: {public_path}")
        except Exception as e:
            st.sidebar.error(f"Erro ao carregar dataset público: {e}")

    if use_wearable:
        try:
            wearable_path = Path(cfg.wearable.path)
            if wearable_path.exists():
                df_wearable = pd.read_json(wearable_path)
            else:
                st.sidebar.warning(f"Dataset wearable não encontrado: {wearable_path}")
        except Exception as e:
            st.sidebar.error(f"Erro ao carregar dataset wearable: {e}")

    # Processar
    if df_public is None and df_wearable is None:
        st.error("Nenhum dataset foi carregado. Verifique os caminhos na configuração.")
        return None

    with st.spinner('⏳ Processando dados... Isso pode levar alguns segundos.'):
        df_processed = preprocess_pipeline(df_public, df_wearable, cfg, validate=False)
    
    # Garantir que a coluna dt seja datetime
    if df_processed is not None and 'dt' in df_processed.columns:
        df_processed['dt'] = pd.to_datetime(df_processed['dt'], errors='coerce')

    return df_processed


def apply_sidebar_filters(df: pd.DataFrame, show_fonte_filter: bool = False) -> pd.DataFrame:
    """
    Aplica filtros da sidebar ao DataFrame.

    Args:
        df: DataFrame processado
        show_fonte_filter: Parâmetro mantido para compatibilidade (não usado)

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
            df = df[df["is_smoker"] == True]
        elif smoker_filter == "Não Fumante":
            df = df[df["is_smoker"] == False]

    # Filtro de praticante
    if "is_practitioner" in df.columns:
        pract_filter = st.sidebar.radio(
            "Status de Praticante", options=["Todos", "Praticante", "Não Praticante"], index=0
        )
        if pract_filter == "Praticante":
            df = df[df["is_practitioner"] == True]
        elif pract_filter == "Não Praticante":
            df = df[df["is_practitioner"] == False]

    # Filtro de período
    if "dt" in df.columns:
        # Remover NaT antes de calcular min/max
        df_with_dates = df[df["dt"].notna()]
        
        if len(df_with_dates) > 0:
            min_date = df_with_dates["dt"].min().date()
            max_date = df_with_dates["dt"].max().date()

            date_range = st.sidebar.date_input(
                "Período",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date,
            )

            if len(date_range) == 2:
                start_date, end_date = date_range
                df = df[(df["dt"].notna()) & (df["dt"].dt.date >= start_date) & (df["dt"].dt.date <= end_date)]

    return df


def show_kpis(df: pd.DataFrame):
    """Exibe KPIs principais no topo do dashboard."""
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_label = "Total de Registros"
        if 'fonte' in df.columns and df['fonte'].nunique() > 1:
            fontes = df['fonte'].value_counts()
            total_label += f"\n({fontes.to_dict()})"
        st.metric(total_label, f"{len(df):,}")

    with col2:
        if "bpm" in df.columns:
            bpm_mean = df["bpm"].mean()
            if pd.notna(bpm_mean):
                st.metric("BPM Médio", f"{bpm_mean:.1f}")
            else:
                st.metric("BPM Médio", "N/A")

    with col3:
        if "pace_min_km" in df.columns:
            pace_mean = df["pace_min_km"].dropna().mean()
            if pd.notna(pace_mean):
                st.metric("Pace Médio", f"{pace_mean:.2f} min/km")
            else:
                st.metric("Pace Médio", "N/A")

    with col4:
        if "is_smoker" in df.columns:
            smoker_pct = (df["is_smoker"] == True).mean() * 100
            st.metric("% Fumantes", f"{smoker_pct:.1f}%")

    with col5:
        if "is_practitioner" in df.columns:
            pract_pct = (df["is_practitioner"] == True).mean() * 100
            st.metric("% Praticantes", f"{pract_pct:.1f}%")


def show_analysis_1(df: pd.DataFrame):
    """
    Análise 1: Fumantes vs Não Fumantes em Esportes.

    Args:
        df: DataFrame processado
    """
    st.header("Análise 1: Fumantes vs Não Fumantes em Esportes")

    st.markdown(
        """
    Comparação do desempenho em atividades esportivas entre fumantes e não fumantes,
    avaliando métricas como pace, BPM, calorias e passos.
    """
    )

    # Filtrar atividades esportivas
    sport_activities = ["Running", "Walking", "Cycling", "Swimming", "Jogging", "Hiking"]
    pattern = "|".join(sport_activities)
    df_sports = df[df["atividade"].str.contains(pattern, case=False, na=False)]

    if len(df_sports) == 0:
        st.warning("Nenhuma atividade esportiva encontrada nos dados filtrados.")
        return

    # Análise
    with st.spinner('🔍 Analisando dados de fumantes...'):
        df_summary, stats_dict = analyze_smokers_vs_nonsmokers(df_sports)
    
    # Verificar se há fumantes nos dados
    n_smokers = len(df_sports[df_sports["is_smoker"] == True])
    n_nonsmokers = len(df_sports[df_sports["is_smoker"] == False])
    
    if n_smokers == 0:
        st.info(f"ℹ️ Dataset atual contém apenas **não fumantes** ({n_nonsmokers:,} registros). Para comparações, use o dataset FitLife (público).")
    elif n_nonsmokers == 0:
        st.info(f"ℹ️ Dataset atual contém apenas **fumantes** ({n_smokers:,} registros).")

    # Mostrar tabela resumo
    st.subheader("Resumo Estatístico")
    st.dataframe(df_summary, width="stretch")

    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribuição de Pace (Boxplot)")
        if "pace_min_km" in df_sports.columns:
            fig = plot_smokers_comparison_boxplot(df_sports, "pace_min_km")
            st.plotly_chart(fig, width="stretch", key="smokers_boxplot")
    
    with col2:
        st.subheader("BPM (Violin Plot)")
        if "bpm" in df_sports.columns:
            fig = plot_smokers_comparison_violin(df_sports, "bpm")
            st.plotly_chart(fig, width="stretch", key="smokers_violin")

    # Testes estatísticos
    if stats_dict and 'metrics' in stats_dict:
        st.subheader("Testes Estatísticos (Mann-Whitney U)")
        metrics_data = []
        for metric, values in stats_dict['metrics'].items():
            metrics_data.append({
                'Métrica': metric,
                'Estatística': f"{values['statistic']:.2f}",
                'P-valor': f"{values['p_value']:.4f}",
                'Significativo (α=0.05)': "✓ Sim" if values['significant'] else "✗ Não"
            })
        stats_df = pd.DataFrame(metrics_data)
        st.dataframe(stats_df, width="stretch")


def show_analysis_2(df: pd.DataFrame):
    """
    Análise 2: Praticantes vs Não Praticantes de Corrida.

    Args:
        df: DataFrame processado
    """
    st.header("Análise 2: Praticantes vs Não Praticantes de Corrida (Pace)")

    st.markdown(
        """
    Comparação do pace (ritmo) e outras métricas entre quem pratica corrida
    e quem não pratica, investigando diferenças de performance.
    """
    )

    # Análise
    with st.spinner('🏃 Analisando dados de corredores...'):
        df_summary, stats_dict = analyze_runners_vs_nonrunners(df)

    if df_summary.empty:
        st.warning("Dados insuficientes para análise de runners.")
        return
    
    # Verificar distribuição de runners
    n_runners = len(df[df["is_runner"] == True])
    n_non_runners = len(df[df["is_runner"] == False])
    
    if n_non_runners == 0:
        st.info(f"ℹ️ Dataset atual contém apenas **corredores** ({n_runners:,} registros).")
    elif n_runners == 0:
        st.info(f"ℹ️ Dataset atual contém apenas **não corredores** ({n_non_runners:,} registros).")

    # Mostrar tabela resumo
    st.subheader("Resumo Estatístico")
    st.dataframe(df_summary, width="stretch")

    # Gráficos
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Distribuição de Pace (Boxplot)")
        if "pace_min_km" in df.columns:
            fig = plot_runners_comparison_boxplot(df, "pace_min_km")
            st.plotly_chart(fig, width="stretch", key="runners_boxplot")

    with col2:
        st.subheader("Distribuição de Pace (Histograma)")
        if "pace_min_km" in df.columns:
            fig = plot_runners_comparison_histogram(df, "pace_min_km")
            st.plotly_chart(fig, width="stretch", key="runners_histogram")

    # Testes estatísticos
    if stats_dict and 'metrics' in stats_dict:
        st.subheader("Testes Estatísticos (Mann-Whitney U)")
        metrics_data = []
        for metric, values in stats_dict['metrics'].items():
            metrics_data.append({
                'Métrica': metric,
                'Estatística': f"{values['statistic']:.2f}",
                'P-valor': f"{values['p_value']:.4f}",
                'Significativo (α=0.05)': "✓ Sim" if values['significant'] else "✗ Não"
            })
        stats_df = pd.DataFrame(metrics_data)
        st.dataframe(stats_df, width="stretch")


def show_analysis_3(df: pd.DataFrame):
    """
    Análise 3: Prática de Esportes por Faixas de Idade.

    Args:
        df: DataFrame processado
    """
    st.header("Análise 3: Prática de Esportes por Faixas de Idade")

    st.markdown(
        """
    Investigação de como a prática de atividades físicas varia entre diferentes
    faixas etárias, incluindo taxas de participação e métricas médias.
    """
    )

    # Análise
    with st.spinner('📊 Analisando prática por faixa etária...'):
        df_rates, df_metrics = analyze_practice_by_age(df)

    if df_rates.empty:
        st.warning("Dados insuficientes para análise por idade.")
        return

    # Mostrar tabela de taxas
    st.subheader("Taxa de Praticantes por Faixa de Idade")
    st.dataframe(df_rates, width="stretch")

    # Gráficos
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Taxa de Prática por Idade")
        fig = plot_practice_by_age_bars_plotly(df_rates)
        st.plotly_chart(fig, width="stretch", key="practice_bars")
    
    with col2:
        st.subheader("Distribuição: Praticantes vs Não Praticantes")
        fig = plot_practice_by_age_stacked(df_rates)
        st.plotly_chart(fig, width="stretch", key="practice_stacked")

    # Métricas médias
    if not df_metrics.empty:
        st.subheader("Métricas Médias por Faixa de Idade (Apenas Praticantes)")
        st.dataframe(df_metrics, width="stretch")


def show_analysis_4(df: pd.DataFrame):
    """
    Análise 4: BPM Praticantes vs Não Praticantes.

    Args:
        df: DataFrame processado
    """
    st.header("Análise 4: Comparação de BPM entre Praticantes e Não Praticantes")

    st.markdown(
        """
    Comparação do BPM médio entre quem pratica atividades físicas e quem não pratica,
    incluindo análise estratificada por faixa etária.
    """
    )

    # Análise
    with st.spinner('💓 Analisando BPM de praticantes...'):
        df_summary, stats_dict = analyze_bpm_practitioners_vs_nonpractitioners(df)

    if df_summary.empty:
        st.warning("Dados insuficientes para análise de BPM.")
        return
    
    # Verificar distribuição de praticantes
    n_practitioners = len(df[df["is_practitioner"] == True])
    n_non_practitioners = len(df[df["is_practitioner"] == False])
    
    if n_non_practitioners == 0:
        st.info(f"ℹ️ Dataset atual contém apenas **praticantes** ({n_practitioners:,} registros). Comparação não disponível.")
    elif n_practitioners == 0:
        st.info(f"ℹ️ Dataset atual contém apenas **não praticantes** ({n_non_practitioners:,} registros).")

    # Mostrar tabela resumo
    st.subheader("Resumo Estatístico Geral")
    st.dataframe(df_summary, width="stretch")

    # Testes estatísticos
    if stats_dict:
        st.subheader("Testes Estatísticos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 't_test' in stats_dict:
                st.markdown("**Teste t**")
                st.metric("Estatística t", f"{stats_dict['t_test']['statistic']:.2f}")
                st.metric("P-valor", f"{stats_dict['t_test']['p_value']:.4f}")
                st.metric("Significativo (α=0.05)", "✓ Sim" if stats_dict['t_test']['significant'] else "✗ Não")
        
        with col2:
            if 'mann_whitney' in stats_dict:
                st.markdown("**Teste Mann-Whitney U**")
                st.metric("Estatística U", f"{stats_dict['mann_whitney']['statistic']:.2f}")
                st.metric("P-valor", f"{stats_dict['mann_whitney']['p_value']:.4f}")
                st.metric("Significativo (α=0.05)", "✓ Sim" if stats_dict['mann_whitney']['significant'] else "✗ Não")
        
        # Tamanho do efeito
        if 'cohens_d' in stats_dict:
            st.subheader("Tamanho do Efeito (Cohen's d)")
            col1, col2 = st.columns(2)
            col1.metric("Cohen's d", f"{stats_dict['cohens_d']:.3f}")
            col2.metric("Interpretação", stats_dict.get('effect_size', 'N/A'))

    # Gráfico de comparação
    st.subheader("Comparação Visual de BPM")
    fig = plot_bpm_practitioners_comparison(df)
    st.plotly_chart(fig, width="stretch", key="bpm_comparison")


def main():
    """Função principal do aplicativo Streamlit."""
    # CSS customizado para interface minimalista
    st.markdown(
        """
        <style>
        /* Remover fundo branco dos cards de métricas */
        [data-testid="stMetricValue"] {
            background-color: transparent;
        }
        
        /* Estilizar container das métricas */
        [data-testid="stMetric"] {
            background-color: transparent;
            border: 1px solid rgba(250, 250, 250, 0.1);
            padding: 12px;
            border-radius: 8px;
        }
        
        /* Títulos mais clean */
        h1 {
            font-weight: 600;
            color: #ffffff;
        }
        h2, h3 {
            font-weight: 500;
            color: #e0e0e0;
        }
        
        /* Tabs mais elegantes */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            padding: 10px 20px;
            font-weight: 500;
            background-color: transparent;
        }
        
        /* Remover fundos brancos de containers */
        .element-container {
            background-color: transparent;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    # Título
    st.title("Dashboard de Análise de Fitness e Saúde")

    st.markdown(
        """
    Análises interativas sobre dados de fitness e saúde, comparando métricas entre diferentes grupos e faixas etárias.
    """
    )

    # Sidebar - Seleção de datasets
    st.sidebar.title("Configurações")
    
    # Botão para limpar cache
    if st.sidebar.button("↻ Limpar Cache"):
        st.cache_data.clear()
        st.rerun()

    # Seleção de dataset (apenas um por vez)
    dataset_option = st.sidebar.radio(
        "Selecione o Dataset",
        options=["Dataset Wearable (JSON)", "Dataset Público (FitLife)"],
        index=0,
        help="Escolha qual dataset você deseja analisar"
    )
    
    # Definir flags baseado na seleção
    use_wearable = dataset_option == "Dataset Wearable (JSON)"
    use_public = dataset_option == "Dataset Público (FitLife)"
    
    # Mostrar informação sobre o dataset selecionado
    dataset_name = "runs_simulated.json" if use_wearable else "fitlife_clean.csv"
    st.sidebar.markdown(f"**Dataset:** {dataset_name}")

    # Carregar dados
    with st.spinner("Carregando e processando dados..."):
        df = load_and_process_data(use_public, use_wearable)

    if df is None or len(df) == 0:
        st.error("Nenhum dado foi carregado. Verifique os caminhos dos arquivos.")
        return

    # Aplicar filtros (não mostrar filtro de fonte quando há apenas um dataset)
    df_filtered = apply_sidebar_filters(df, show_fonte_filter=False)

    st.sidebar.markdown(f"**Registros após filtros:** {len(df_filtered):,}")

    # Mostrar KPIs
    show_kpis(df_filtered)
    st.markdown("---")

    # Abas de análise
    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Fumantes vs Não Fumantes",
            "Runners vs Não Runners",
            "Prática por Idade",
            "BPM Praticantes",
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
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
    <div style='text-align: center; color: #888;'>
        <small>Dashboard desenvolvido com Streamlit | Python + Plotly + Pandas</small>
    </div>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()

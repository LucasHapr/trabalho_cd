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

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.analysis_v2 import (
    analyze_bpm_practitioners_vs_nonpractitioners,
    analyze_practice_by_age,
    analyze_runners_vs_nonrunners,
    analyze_smokers_vs_nonsmokers,
)
from src.plots_v2 import (
    plot_bpm_by_age_heatmap,
    plot_bpm_practitioners_comparison,
    plot_practice_by_age_bars,
    plot_practice_by_age_stacked,
    plot_runners_comparison_boxplot,
    plot_runners_comparison_histogram,
    plot_smokers_comparison_boxplot,
    plot_smokers_comparison_violin,
)

# Configuração da página
st.set_page_config(
    page_title="Dashboard Fitness & Saúde V2",
    page_icon="🏃",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def load_data():
    """Carrega o dataset fitlife_clean.csv com cache."""
    data_path = Path("data/external/fitlife_clean.csv")
    
    if not data_path.exists():
        st.error(f"❌ Arquivo não encontrado: {data_path}")
        st.stop()
    
    df = pd.read_csv(data_path)
    df['dt'] = pd.to_datetime(df['dt'])
    return df


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica filtros da sidebar ao dataset."""
    df_filtered = df.copy()
    
    # Filtro de faixa de idade
    st.sidebar.subheader("🎯 Filtros")
    
    age_groups = df['faixa_idade'].dropna().unique().tolist()
    age_groups.sort()
    selected_ages = st.sidebar.multiselect(
        "Faixas de Idade",
        options=age_groups,
        default=age_groups
    )
    
    if selected_ages:
        df_filtered = df_filtered[df_filtered['faixa_idade'].isin(selected_ages)]
    
    # Filtro de fumante
    filter_smoker = st.sidebar.selectbox(
        "Filtrar por Fumante",
        options=["Todos", "Apenas Fumantes", "Apenas Não Fumantes"]
    )
    
    if filter_smoker == "Apenas Fumantes":
        df_filtered = df_filtered[df_filtered['is_smoker'] == True]
    elif filter_smoker == "Apenas Não Fumantes":
        df_filtered = df_filtered[df_filtered['is_smoker'] == False]
    
    # Filtro de período
    st.sidebar.subheader("📅 Período")
    
    min_date = df['dt'].min().date()
    max_date = df['dt'].max().date()
    
    date_range = st.sidebar.date_input(
        "Selecione o período",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        df_filtered = df_filtered[
            (df_filtered['dt'].dt.date >= start_date) &
            (df_filtered['dt'].dt.date <= end_date)
        ]
    
    return df_filtered


def show_kpis(df: pd.DataFrame):
    """Exibe KPIs principais no topo do dashboard."""
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total de Registros", f"{len(df):,}")
    
    with col2:
        taxa_fumantes = df['is_smoker'].mean() * 100
        st.metric("Taxa de Fumantes", f"{taxa_fumantes:.1f}%")
    
    with col3:
        taxa_runners = df['is_runner'].mean() * 100
        st.metric("Taxa de Corredores", f"{taxa_runners:.1f}%")
    
    with col4:
        taxa_praticantes = df['is_practitioner'].mean() * 100
        st.metric("Taxa de Praticantes", f"{taxa_praticantes:.1f}%")
    
    with col5:
        bpm_medio = df['bpm'].mean()
        st.metric("BPM Médio", f"{bpm_medio:.1f}")


def show_analysis_1(df: pd.DataFrame):
    """Análise 1: Fumantes vs Não Fumantes."""
    st.header("📊 Análise 1: Fumantes vs Não Fumantes")
    st.markdown("Comparação de métricas de saúde entre fumantes e não fumantes.")
    
    # Executar análise
    df_summary, stats = analyze_smokers_vs_nonsmokers(df)
    
    # Mostrar resumo
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Resultados")
        st.dataframe(df_summary, use_container_width=True)
    
    with col2:
        st.subheader("🧪 Testes Estatísticos")
        for metric, result in stats['metrics'].items():
            sig = "✅ Significativo" if result['significant'] else "❌ Não significativo"
            st.write(f"**{metric}**: p-value = {result['p_value']:.4f} {sig}")
    
    # Visualizações
    st.subheader("📊 Visualizações Interativas")
    
    tab1, tab2 = st.tabs(["BPM", "Calorias"])
    
    with tab1:
        fig_bpm_box = plot_smokers_comparison_boxplot(df, 'bpm')
        st.plotly_chart(fig_bpm_box, use_container_width=True)
    
    with tab2:
        fig_cal_violin = plot_smokers_comparison_violin(df, 'calorias_kcal')
        st.plotly_chart(fig_cal_violin, use_container_width=True)


def show_analysis_2(df: pd.DataFrame):
    """Análise 2: Runners vs Não Runners."""
    st.header("🏃 Análise 2: Corredores vs Não Corredores")
    st.markdown("Comparação de métricas entre praticantes e não praticantes de corrida.")
    
    # Executar análise
    df_summary, stats = analyze_runners_vs_nonrunners(df)
    
    # Mostrar resumo
    st.subheader("📈 Resultados")
    st.dataframe(df_summary, use_container_width=True)
    
    # Testes estatísticos
    with st.expander("🧪 Ver Testes Estatísticos"):
        for metric, tests in stats.items():
            st.write(f"### {metric.upper()}")
            mw = tests['mann_whitney']
            ks = tests['kolmogorov_smirnov']
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Mann-Whitney U**")
                st.write(f"p-value: {mw['p_value']:.4f}")
                st.write(f"Significativo: {'Sim ✅' if mw['significant'] else 'Não ❌'}")
            
            with col2:
                st.write("**Kolmogorov-Smirnov**")
                st.write(f"p-value: {ks['p_value']:.4f}")
                st.write(f"Significativo: {'Sim ✅' if ks['significant'] else 'Não ❌'}")
    
    # Visualizações
    st.subheader("📊 Visualizações Interativas")
    
    tab1, tab2 = st.tabs(["BPM (Boxplot)", "Calorias (Histograma)"])
    
    with tab1:
        fig_bpm = plot_runners_comparison_boxplot(df, 'bpm')
        st.plotly_chart(fig_bpm, use_container_width=True)
    
    with tab2:
        fig_cal = plot_runners_comparison_histogram(df, 'calorias_kcal')
        st.plotly_chart(fig_cal, use_container_width=True)


def show_analysis_3(df: pd.DataFrame):
    """Análise 3: Prática por Faixa de Idade."""
    st.header("👥 Análise 3: Prática de Esportes por Faixa de Idade")
    st.markdown("Taxa de praticantes e métricas de saúde por faixa etária.")
    
    # Executar análise
    df_summary, stats = analyze_practice_by_age(df)
    
    # Mostrar resumo
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📈 Resultados por Faixa de Idade")
        st.dataframe(df_summary, use_container_width=True)
    
    with col2:
        st.subheader("📊 Estatísticas Globais")
        st.metric("Total de Pessoas", f"{stats['total_pessoas']:,}")
        st.metric("Taxa Global de Praticantes", f"{stats['taxa_global_pct']:.1f}%")
        st.metric("BPM Médio Global", f"{stats['bpm_global_mean']:.1f}")
        
        if stats['chi2_test']:
            chi2 = stats['chi2_test']
            st.write(f"**Teste Chi-quadrado**")
            st.write(f"p-value: {chi2['p_value']:.4f}")
            st.write(f"Significativo: {'Sim ✅' if chi2['significant'] else 'Não ❌'}")
    
    # Visualizações
    st.subheader("📊 Visualizações Interativas")
    
    tab1, tab2 = st.tabs(["Taxa de Praticantes", "Distribuição (Stacked)"])
    
    with tab1:
        fig_bars = plot_practice_by_age_bars(df_summary)
        st.plotly_chart(fig_bars, use_container_width=True)
    
    with tab2:
        fig_stacked = plot_practice_by_age_stacked(df_summary)
        st.plotly_chart(fig_stacked, use_container_width=True)


def show_analysis_4(df: pd.DataFrame):
    """Análise 4: BPM Praticantes vs Não Praticantes."""
    st.header("💓 Análise 4: BPM - Praticantes vs Não Praticantes")
    st.markdown("Comparação de BPM médio entre praticantes e não praticantes de atividades físicas.")
    
    # Executar análise
    df_global, df_by_age, stats = analyze_bpm_practitioners_vs_nonpractitioners(df)
    
    # Mostrar resumo
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📈 Comparação Global")
        st.dataframe(df_global, use_container_width=True)
    
    with col2:
        st.subheader("🧪 Testes Estatísticos")
        
        if 't_test' in stats:
            st.write("**T-test**")
            st.write(f"p-value: {stats['t_test']['p_value']:.4f}")
            st.write(f"Significativo: {'Sim ✅' if stats['t_test']['significant'] else 'Não ❌'}")
            
            st.write("**Cohen's d**")
            st.write(f"{stats['cohens_d']:.3f} ({stats['effect_size']} effect)")
    
    # Por faixa de idade
    st.subheader("📊 BPM por Faixa de Idade")
    st.dataframe(df_by_age, use_container_width=True)
    
    # Visualizações
    st.subheader("📊 Visualizações Interativas")
    
    tab1, tab2 = st.tabs(["Comparação Global", "Heatmap por Idade"])
    
    with tab1:
        fig_comp = plot_bpm_practitioners_comparison(df_global)
        st.plotly_chart(fig_comp, use_container_width=True)
    
    with tab2:
        fig_heatmap = plot_bpm_by_age_heatmap(df_by_age)
        st.plotly_chart(fig_heatmap, use_container_width=True)


def main():
    """Função principal do dashboard."""
    # Título
    st.title("🏃 Dashboard de Análise de Fitness e Saúde")
    st.markdown("**Análise completa do dataset FitLife**")
    st.markdown("---")
    
    # Carregar dados
    with st.spinner("Carregando dados..."):
        df = load_data()
    
    # Aplicar filtros
    df_filtered = apply_filters(df)
    
    # Mostrar info sobre filtros
    if len(df_filtered) < len(df):
        st.sidebar.success(f"✅ {len(df_filtered):,} registros selecionados de {len(df):,}")
    else:
        st.sidebar.info(f"📊 Total: {len(df):,} registros")
    
    # KPIs
    show_kpis(df_filtered)
    st.markdown("---")
    
    # Tabs principais
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Análise 1: Fumantes",
        "🏃 Análise 2: Corredores",
        "👥 Análise 3: Faixa de Idade",
        "💓 Análise 4: BPM"
    ])
    
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
    st.markdown("**Dashboard criado com Streamlit | Dados: FitLife Dataset**")


if __name__ == "__main__":
    main()

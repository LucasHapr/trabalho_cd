"""
Script para executar o pipeline completo de forma standalone.

Este script pode ser executado diretamente para processar dados,
executar análises e gerar visualizações sem usar o Streamlit.
"""

import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent))

from hydra import compose, initialize_config_dir

from src.analysis import run_all_analyses
from src.dataio import load_data, save_parquet
from src.modeling import train_and_evaluate_models
from src.plots import generate_all_plots
from src.preprocess import preprocess_pipeline


def main():
    """Executa o pipeline completo."""
    print("\n" + "=" * 80)
    print("🚀 PIPELINE COMPLETO DE CIÊNCIA DE DADOS - FITNESS & SAÚDE")
    print("=" * 80)

    # Inicializar Hydra
    config_dir = Path(__file__).parent / "conf"
    with initialize_config_dir(config_dir=str(config_dir.absolute()), version_base=None):
        cfg = compose(config_name="config")

    print(f"\n📋 Configuração:")
    print(f"  - Usar dataset público: {cfg.use_public}")
    print(f"  - Usar dataset wearable: {cfg.use_wearable}")

    # 1. Carregar dados
    print("\n" + "=" * 80)
    print("📖 ETAPA 1: CARREGANDO DADOS")
    print("=" * 80)

    df_public = None
    df_wearable = None

    if cfg.use_public:
        try:
            public_path = Path(cfg.external.path)
            if public_path.exists():
                df_public = load_data(public_path)
                print(f"✓ Dataset público carregado: {len(df_public)} linhas")
            else:
                print(f"⚠️  Dataset público não encontrado: {public_path}")
        except Exception as e:
            print(f"✗ Erro ao carregar dataset público: {e}")

    if cfg.use_wearable:
        try:
            wearable_path = Path(cfg.wearable.path)
            if wearable_path.exists():
                df_wearable = load_data(wearable_path)
                print(f"✓ Dataset wearable carregado: {len(df_wearable)} linhas")
            else:
                print(f"⚠️  Dataset wearable não encontrado: {wearable_path}")
        except Exception as e:
            print(f"✗ Erro ao carregar dataset wearable: {e}")

    if df_public is None and df_wearable is None:
        print("\n❌ ERRO: Nenhum dataset foi carregado. Verifique os caminhos.")
        return

    # 2. Preprocessar dados
    print("\n" + "=" * 80)
    print("⚙️  ETAPA 2: PREPROCESSAMENTO")
    print("=" * 80)

    df_processed = preprocess_pipeline(df_public, df_wearable, cfg, validate=True)

    # Salvar dados processados
    output_path = Path(cfg.output.processed_data) / "combined_data.parquet"
    save_parquet(df_processed, output_path)
    print(f"\n✓ Dados processados salvos: {output_path}")

    # 3. Executar análises
    print("\n" + "=" * 80)
    print("📊 ETAPA 3: ANÁLISES ESTATÍSTICAS")
    print("=" * 80)

    results = run_all_analyses(df_processed, cfg.sport_activities)

    # Salvar resultados
    results_dir = Path(cfg.output.reports)
    results_dir.mkdir(parents=True, exist_ok=True)

    # Salvar tabelas de resumo
    for analysis_name, analysis_data in results.items():
        if "summary" in analysis_data and not analysis_data["summary"].empty:
            csv_path = results_dir / f"{analysis_name}_summary.csv"
            analysis_data["summary"].to_csv(csv_path, index=False)
            print(f"  💾 {csv_path}")

    # 4. Gerar visualizações
    print("\n" + "=" * 80)
    print("🎨 ETAPA 4: VISUALIZAÇÕES")
    print("=" * 80)

    all_figs = generate_all_plots(
        df_processed, results, output_dir=cfg.output.reports, save_interactive=True, save_static=True
    )

    print(f"\n✓ {sum(len(figs) for figs in all_figs.values())} visualizações geradas")

    # 5. Treinar modelos (opcional)
    print("\n" + "=" * 80)
    print("🤖 ETAPA 5: MODELAGEM PREDITIVA")
    print("=" * 80)

    try:
        models = train_and_evaluate_models(
            df_processed, targets=["bpm", "calorias_kcal"], save_dir=Path(cfg.output.models)
        )
        print(f"\n✓ {len(models)} modelos treinados")
    except Exception as e:
        print(f"\n⚠️  Modelagem pulada: {e}")

    # Resumo final
    print("\n" + "=" * 80)
    print("✅ PIPELINE CONCLUÍDO COM SUCESSO!")
    print("=" * 80)
    print(f"\n📊 Resumo:")
    print(f"  - Registros processados: {len(df_processed):,}")
    print(f"  - Análises executadas: 4")
    print(f"  - Visualizações geradas: {sum(len(figs) for figs in all_figs.values())}")
    print(f"  - Dados salvos em: {cfg.output.processed_data}")
    print(f"  - Relatórios em: {cfg.output.reports}")

    print("\n🎉 Para visualizar os resultados:")
    print("   streamlit run app.py")


if __name__ == "__main__":
    main()

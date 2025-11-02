"""
Script para criar um dataset de exemplo para teste.

Este script gera dados sintéticos no formato esperado pelo projeto
para fins de teste e demonstração.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from random import choice, randint, uniform

import pandas as pd


def generate_sample_public_data(n_samples: int = 500) -> pd.DataFrame:
    """
    Gera dataset público sintético.

    Args:
        n_samples: Número de amostras a gerar

    Returns:
        DataFrame com dados sintéticos
    """
    print(f"📝 Gerando {n_samples} registros sintéticos (dataset público)...")

    data = {
        "ID": [f"P{i:04d}" for i in range(n_samples)],
        "Data": [
            (datetime.now() - timedelta(days=randint(0, 365))).strftime("%Y-%m-%d")
            for _ in range(n_samples)
        ],
        "Idade": [randint(18, 70) for _ in range(n_samples)],
        "Gênero": [choice(["M", "F"]) for _ in range(n_samples)],
        "Altura": [uniform(150, 190) for _ in range(n_samples)],
        "Peso": [uniform(50, 100) for _ in range(n_samples)],
        "Duração": [uniform(10, 120) for _ in range(n_samples)],
        "Calorias Queimadas": [uniform(100, 800) for _ in range(n_samples)],
        "BPM": [uniform(80, 180) for _ in range(n_samples)],
        "Passos": [randint(0, 15000) for _ in range(n_samples)],
        "Condição de Saúde": [choice(["Excelente", "Bom", "Regular"]) for _ in range(n_samples)],
        "Nível de Fumante": [
            choice(["Não Fumante", "Ex-fumante", "Fumante Leve", "Fumante Moderado"])
            for _ in range(n_samples)
        ],
        "Tipo de Atividade": [
            choice(["Running", "Walking", "Cycling", "Swimming", "Resting"])
            for _ in range(n_samples)
        ],
    }

    df = pd.DataFrame(data)

    # Adicionar distância para atividades físicas
    df["Distancia"] = 0.0
    mask = df["Tipo de Atividade"].isin(["Running", "Walking", "Cycling"])
    df.loc[mask, "Distancia"] = df.loc[mask, "Duração"] / uniform(8, 15)

    return df


def generate_sample_wearable_data(n_samples: int = 200) -> list:
    """
    Gera dataset wearable sintético (JSON).

    Args:
        n_samples: Número de amostras a gerar

    Returns:
        Lista de dicionários com dados sintéticos
    """
    print(f"📝 Gerando {n_samples} registros sintéticos (dataset wearable)...")

    data = []

    for i in range(n_samples):
        record = {
            "id": f"R{i:04d}",
            "data": (datetime.now() - timedelta(days=randint(0, 180))).strftime("%Y-%m-%d"),
            "idade": randint(20, 60),
            "genero": choice(["M", "F"]),
            "altura_cm": uniform(155, 185),
            "peso_kg": uniform(55, 95),
            "distancia_km": uniform(3, 15),
            "duracao_min": uniform(20, 90),
            "calorias_kcal": uniform(200, 900),
            "bpm_medio": uniform(120, 170),
            "passos": randint(3000, 18000),
            "condicao_saude": choice(["Excelente", "Bom", "Regular"]),
            "nivel_fumante": choice(["Não Fumante", "Ex-fumante", "Fumante Leve"]),
        }

        # Ajustar pace de forma coerente
        record["duracao_min"] = record["distancia_km"] * uniform(5, 8)

        data.append(record)

    return data


def main():
    """Gera datasets de exemplo."""
    print("\n" + "=" * 60)
    print("🎲 GERANDO DATASETS SINTÉTICOS DE EXEMPLO")
    print("=" * 60)

    base_path = Path(__file__).parent

    # 1. Dataset público
    df_public = generate_sample_public_data(500)
    public_path = base_path / "data" / "external" / "fitlife_sample.csv"
    public_path.parent.mkdir(parents=True, exist_ok=True)
    df_public.to_csv(public_path, index=False, encoding="utf-8")
    print(f"✅ Dataset público salvo: {public_path}")
    print(f"   {len(df_public)} linhas, {len(df_public.columns)} colunas")

    # 2. Dataset wearable
    wearable_data = generate_sample_wearable_data(200)
    wearable_path = base_path / "data" / "runs_simulated.json"

    # Verificar se já existe
    if wearable_path.exists():
        print(f"\n⚠️  Arquivo já existe: {wearable_path}")
        overwrite = input("Deseja sobrescrever? (s/N): ").lower()
        if overwrite != "s":
            print("❌ Operação cancelada")
            return

    with open(wearable_path, "w", encoding="utf-8") as f:
        json.dump(wearable_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Dataset wearable salvo: {wearable_path}")
    print(f"   {len(wearable_data)} registros")

    print("\n" + "=" * 60)
    print("✅ DATASETS CRIADOS COM SUCESSO!")
    print("=" * 60)
    print("\n💡 Próximos passos:")
    print("1. Verifique os arquivos gerados")
    print("2. Execute: streamlit run app.py")
    print("3. Ou execute: python run_pipeline.py")


if __name__ == "__main__":
    main()

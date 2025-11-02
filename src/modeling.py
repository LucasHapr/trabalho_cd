"""
Módulo de modelagem preditiva.

Este módulo implementa modelos LightGBM para prever BPM e Calorias
a partir de features disponíveis.
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import joblib
import lightgbm as lgb
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


def prepare_features(
    df: pd.DataFrame, target_col: str = "bpm", categorical_cols: Optional[List[str]] = None
) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Prepara features para modelagem.

    Args:
        df: DataFrame processado
        target_col: Coluna alvo (target)
        categorical_cols: Lista de colunas categóricas

    Returns:
        Tupla (X, y) com features e target
    """
    print(f"\n🔧 Preparando features para prever '{target_col}'...")

    # Filtrar linhas com target válido
    df_model = df[df[target_col].notna()].copy()
    print(f"  Linhas com target válido: {len(df_model)}")

    # Definir colunas de features
    numeric_features = [
        "idade",
        "altura_cm",
        "peso_kg",
        "duracao_min",
        "distancia_km",
        "passos",
        "imc",
        "pace_min_km",
        "cadencia_passos_min",
    ]

    if categorical_cols is None:
        categorical_cols = ["genero", "faixa_idade", "condicao_saude", "nivel_fumante", "atividade"]

    boolean_features = ["is_runner", "is_practitioner", "is_smoker"]

    # Selecionar features disponíveis
    available_numeric = [f for f in numeric_features if f in df_model.columns and f != target_col]
    available_categorical = [f for f in categorical_cols if f in df_model.columns]
    available_boolean = [f for f in boolean_features if f in df_model.columns]

    print(f"  Features numéricas: {len(available_numeric)}")
    print(f"  Features categóricas: {len(available_categorical)}")
    print(f"  Features booleanas: {len(available_boolean)}")

    # Criar DataFrame de features
    X = pd.DataFrame()

    # Adicionar numéricas
    for col in available_numeric:
        X[col] = df_model[col].fillna(df_model[col].median())

    # Adicionar booleanas (converter para int)
    for col in available_boolean:
        X[col] = df_model[col].astype(int)

    # One-hot encoding para categóricas
    for col in available_categorical:
        dummies = pd.get_dummies(df_model[col], prefix=col, drop_first=True)
        X = pd.concat([X, dummies], axis=1)

    # Target
    y = df_model[target_col]

    print(f"  Shape final: X={X.shape}, y={y.shape}")

    return X, y


def train_lightgbm_model(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float = 0.2,
    random_state: int = 42,
    lgb_params: Optional[Dict] = None,
) -> Tuple[lgb.Booster, Dict]:
    """
    Treina modelo LightGBM.

    Args:
        X: Features
        y: Target
        test_size: Proporção do conjunto de teste
        random_state: Seed para reprodutibilidade
        lgb_params: Parâmetros do LightGBM

    Returns:
        Tupla (model, results_dict) com modelo e métricas
    """
    print(f"\n🚀 Treinando modelo LightGBM...")

    # Split train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    print(f"  Train: {len(X_train)} amostras")
    print(f"  Test: {len(X_test)} amostras")

    # Parâmetros padrão
    if lgb_params is None:
        lgb_params = {
            "objective": "regression",
            "metric": "rmse",
            "num_leaves": 31,
            "learning_rate": 0.05,
            "feature_fraction": 0.9,
            "bagging_fraction": 0.8,
            "bagging_freq": 5,
            "verbose": -1,
        }

    # Criar datasets
    train_data = lgb.Dataset(X_train, label=y_train)
    test_data = lgb.Dataset(X_test, label=y_test, reference=train_data)

    # Treinar
    print("  Treinando...")
    model = lgb.train(
        lgb_params,
        train_data,
        num_boost_round=100,
        valid_sets=[train_data, test_data],
        valid_names=["train", "test"],
        callbacks=[lgb.early_stopping(stopping_rounds=10), lgb.log_evaluation(period=0)],
    )

    # Predições
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    # Métricas
    results = {
        "train": {
            "mae": mean_absolute_error(y_train, y_train_pred),
            "rmse": np.sqrt(mean_squared_error(y_train, y_train_pred)),
            "r2": r2_score(y_train, y_train_pred),
        },
        "test": {
            "mae": mean_absolute_error(y_test, y_test_pred),
            "rmse": np.sqrt(mean_squared_error(y_test, y_test_pred)),
            "r2": r2_score(y_test, y_test_pred),
        },
        "feature_importance": dict(
            zip(X.columns, model.feature_importance(importance_type="gain"))
        ),
        "predictions": {"y_test": y_test, "y_test_pred": y_test_pred},
    }

    print("\n📈 Resultados:")
    print(f"  Train - MAE: {results['train']['mae']:.2f}, RMSE: {results['train']['rmse']:.2f}, R²: {results['train']['r2']:.3f}")
    print(f"  Test  - MAE: {results['test']['mae']:.2f}, RMSE: {results['test']['rmse']:.2f}, R²: {results['test']['r2']:.3f}")

    return model, results


def save_model(
    model: lgb.Booster, filepath: Union[str, Path], feature_names: Optional[List[str]] = None
) -> None:
    """
    Salva modelo treinado.

    Args:
        model: Modelo LightGBM
        filepath: Caminho do arquivo de saída
        feature_names: Lista de nomes das features
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    # Salvar modelo
    model.save_model(str(filepath))
    print(f"💾 Modelo salvo: {filepath}")

    # Salvar metadata
    if feature_names:
        metadata = {"feature_names": feature_names}
        metadata_path = filepath.with_suffix(".metadata.pkl")
        joblib.dump(metadata, metadata_path)
        print(f"💾 Metadata salvo: {metadata_path}")


def load_model(filepath: Union[str, Path]) -> Tuple[lgb.Booster, Optional[Dict]]:
    """
    Carrega modelo salvo.

    Args:
        filepath: Caminho do arquivo do modelo

    Returns:
        Tupla (model, metadata)
    """
    filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"Modelo não encontrado: {filepath}")

    # Carregar modelo
    model = lgb.Booster(model_file=str(filepath))
    print(f"📖 Modelo carregado: {filepath}")

    # Carregar metadata se existir
    metadata_path = filepath.with_suffix(".metadata.pkl")
    metadata = None
    if metadata_path.exists():
        metadata = joblib.load(metadata_path)
        print(f"📖 Metadata carregado: {metadata_path}")

    return model, metadata


def train_and_evaluate_models(
    df: pd.DataFrame, targets: List[str] = ["bpm", "calorias_kcal"], save_dir: Optional[Path] = None
) -> Dict:
    """
    Treina e avalia modelos para múltiplos targets.

    Args:
        df: DataFrame processado
        targets: Lista de colunas target
        save_dir: Diretório para salvar modelos

    Returns:
        Dicionário com modelos e resultados
    """
    print("\n" + "=" * 60)
    print("🤖 TREINANDO MODELOS PREDITIVOS")
    print("=" * 60)

    all_results = {}

    for target in targets:
        if target not in df.columns:
            print(f"\n⚠️  Target '{target}' não encontrado, pulando...")
            continue

        print(f"\n{'=' * 60}")
        print(f"Target: {target}")
        print(f"{'=' * 60}")

        try:
            # Preparar features
            X, y = prepare_features(df, target_col=target)

            if len(X) < 50:
                print(f"⚠️  Dados insuficientes para treinar modelo (n={len(X)})")
                continue

            # Treinar modelo
            model, results = train_lightgbm_model(X, y)

            # Salvar
            if save_dir:
                save_dir = Path(save_dir)
                model_path = save_dir / f"lightgbm_{target}.txt"
                save_model(model, model_path, feature_names=list(X.columns))

            all_results[target] = {"model": model, "results": results, "feature_names": list(X.columns)}

        except Exception as e:
            print(f"✗ Erro ao treinar modelo para {target}: {e}")
            continue

    print("\n" + "=" * 60)
    print(f"✅ TREINAMENTO CONCLUÍDO: {len(all_results)} modelos")
    print("=" * 60)

    return all_results


def get_feature_importance_df(results: Dict, target: str, top_n: int = 10) -> pd.DataFrame:
    """
    Extrai importância das features como DataFrame.

    Args:
        results: Dicionário de resultados
        target: Nome do target
        top_n: Número de top features a retornar

    Returns:
        DataFrame com features e importâncias
    """
    if target not in results:
        return pd.DataFrame()

    feature_importance = results[target]["results"]["feature_importance"]

    df_importance = pd.DataFrame(
        {"feature": list(feature_importance.keys()), "importance": list(feature_importance.values())}
    )

    df_importance = df_importance.sort_values("importance", ascending=False).head(top_n)

    return df_importance


if __name__ == "__main__":
    print("✓ Módulo modeling carregado com sucesso")

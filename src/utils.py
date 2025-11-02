"""
Módulo de funções utilitárias.

Este módulo fornece funções auxiliares para transformações, binning,
divisões seguras e outras operações comuns.
"""

from typing import List, Optional, Union

import numpy as np
import pandas as pd


def safe_div(
    numerator: Union[float, np.ndarray, pd.Series],
    denominator: Union[float, np.ndarray, pd.Series],
    default: float = np.nan,
) -> Union[float, np.ndarray, pd.Series]:
    """
    Realiza divisão segura, retornando default quando denominador é zero.

    Args:
        numerator: Numerador da divisão
        denominator: Denominador da divisão
        default: Valor padrão quando denominador é zero

    Returns:
        Resultado da divisão ou default

    Examples:
        >>> safe_div(10, 2)
        5.0
        >>> safe_div(10, 0)
        nan
        >>> safe_div(10, 0, default=0)
        0.0
    """
    if isinstance(denominator, (pd.Series, np.ndarray)):
        result = np.where(denominator != 0, numerator / denominator, default)
        if isinstance(numerator, pd.Series):
            return pd.Series(result, index=numerator.index)
        return result
    else:
        return numerator / denominator if denominator != 0 else default


def bin_ages(
    ages: Union[pd.Series, np.ndarray],
    bins: Optional[List[int]] = None,
    labels: Optional[List[str]] = None,
) -> pd.Series:
    """
    Agrupa idades em faixas etárias.

    Args:
        ages: Série ou array com idades
        bins: Limites das faixas (default: [0, 17, 24, 34, 44, 54, 64, 120])
        labels: Rótulos das faixas (default: ["<=17", "18-24", ...])

    Returns:
        Série categórica com faixas etárias

    Examples:
        >>> ages = pd.Series([15, 25, 35, 45, 55, 65])
        >>> bin_ages(ages)
        0     <=17
        1    18-24
        2    25-34
        3    35-44
        4    45-54
        5    55-64
        dtype: category
    """
    if bins is None:
        bins = [0, 17, 24, 34, 44, 54, 64, 120]

    if labels is None:
        labels = ["<=17", "18-24", "25-34", "35-44", "45-54", "55-64", "65+"]

    return pd.cut(ages, bins=bins, labels=labels, include_lowest=True)


def calculate_imc(
    peso_kg: Union[pd.Series, np.ndarray], altura_cm: Union[pd.Series, np.ndarray]
) -> Union[pd.Series, np.ndarray]:
    """
    Calcula o Índice de Massa Corporal (IMC).

    IMC = peso(kg) / (altura(m))^2

    Args:
        peso_kg: Peso em kilogramas
        altura_cm: Altura em centímetros

    Returns:
        IMC calculado

    Examples:
        >>> calculate_imc(70, 170)
        24.22
    """
    altura_m = altura_cm / 100
    return safe_div(peso_kg, altura_m**2, default=np.nan)


def calculate_pace(
    duracao_min: Union[pd.Series, np.ndarray], distancia_km: Union[pd.Series, np.ndarray]
) -> Union[pd.Series, np.ndarray]:
    """
    Calcula o pace (ritmo) em minutos por quilômetro.

    Args:
        duracao_min: Duração em minutos
        distancia_km: Distância em quilômetros

    Returns:
        Pace em min/km

    Examples:
        >>> calculate_pace(30, 5)
        6.0
    """
    return safe_div(duracao_min, distancia_km, default=np.nan)


def calculate_cadence(
    passos: Union[pd.Series, np.ndarray], duracao_min: Union[pd.Series, np.ndarray]
) -> Union[pd.Series, np.ndarray]:
    """
    Calcula a cadência (passos por minuto).

    Args:
        passos: Número de passos
        duracao_min: Duração em minutos

    Returns:
        Cadência em passos/min

    Examples:
        >>> calculate_cadence(1800, 30)
        60.0
    """
    return safe_div(passos, duracao_min, default=np.nan)


def calculate_speed_kmh(
    distancia_km: Union[pd.Series, np.ndarray], duracao_min: Union[pd.Series, np.ndarray]
) -> Union[pd.Series, np.ndarray]:
    """
    Calcula a velocidade em km/h.

    Args:
        distancia_km: Distância em quilômetros
        duracao_min: Duração em minutos

    Returns:
        Velocidade em km/h

    Examples:
        >>> calculate_speed_kmh(10, 60)
        10.0
    """
    duracao_h = duracao_min / 60
    return safe_div(distancia_km, duracao_h, default=np.nan)


def classify_imc(imc: Union[pd.Series, np.ndarray]) -> Union[pd.Series, np.ndarray]:
    """
    Classifica o IMC em categorias.

    Args:
        imc: Índice de Massa Corporal

    Returns:
        Categoria do IMC

    Categories:
        - Abaixo do peso: IMC < 18.5
        - Peso normal: 18.5 <= IMC < 25
        - Sobrepeso: 25 <= IMC < 30
        - Obesidade: IMC >= 30
    """
    if isinstance(imc, pd.Series):
        return pd.cut(
            imc,
            bins=[0, 18.5, 25, 30, 100],
            labels=["Abaixo do peso", "Peso normal", "Sobrepeso", "Obesidade"],
            include_lowest=True,
        )
    else:
        conditions = [imc < 18.5, (imc >= 18.5) & (imc < 25), (imc >= 25) & (imc < 30), imc >= 30]
        choices = ["Abaixo do peso", "Peso normal", "Sobrepeso", "Obesidade"]
        return np.select(conditions, choices, default="Desconhecido")


def is_smoker_from_level(nivel_fumante: pd.Series) -> pd.Series:
    """
    Determina se é fumante baseado no nível de fumante.

    Args:
        nivel_fumante: Série com níveis de fumante

    Returns:
        Série booleana indicando se é fumante

    Examples:
        >>> df = pd.DataFrame({'nivel': ['Não Fumante', 'Fumante Leve', 'Ex-fumante']})
        >>> is_smoker_from_level(df['nivel'])
        0    False
        1     True
        2    False
        dtype: bool
    """
    if not isinstance(nivel_fumante, pd.Series):
        nivel_fumante = pd.Series(nivel_fumante)

    return nivel_fumante.str.contains("Fumante", case=False, na=False) & ~nivel_fumante.str.contains(
        "Não|Ex", case=False, na=False
    )


def is_runner_from_activity(atividade: pd.Series) -> pd.Series:
    """
    Determina se pratica corrida baseado no tipo de atividade.

    Args:
        atividade: Série com tipos de atividade

    Returns:
        Série booleana indicando se pratica corrida

    Examples:
        >>> df = pd.DataFrame({'ativ': ['Running', 'Walking', 'Running']})
        >>> is_runner_from_activity(df['ativ'])
        0     True
        1    False
        2     True
        dtype: bool
    """
    if not isinstance(atividade, pd.Series):
        atividade = pd.Series(atividade)

    return atividade.str.contains("Running|Jogging|Corrida", case=False, na=False)


def is_practitioner_from_features(
    atividade: Optional[pd.Series] = None,
    passos: Optional[pd.Series] = None,
    duracao_min: Optional[pd.Series] = None,
    min_passos: int = 1000,
    min_duracao: float = 20.0,
    sport_activities: Optional[List[str]] = None,
) -> pd.Series:
    """
    Determina se é praticante de atividade física.

    Regras:
    - Pratica atividade esportiva listada, OU
    - Possui >= min_passos passos, OU
    - Possui >= min_duracao minutos de atividade

    Args:
        atividade: Série com tipos de atividade
        passos: Série com número de passos
        duracao_min: Série com duração em minutos
        min_passos: Mínimo de passos para ser considerado praticante
        min_duracao: Mínima duração (min) para ser considerado praticante
        sport_activities: Lista de atividades consideradas esportivas

    Returns:
        Série booleana indicando se é praticante
    """
    if sport_activities is None:
        sport_activities = ["Running", "Walking", "Cycling", "Swimming", "Jogging", "Hiking"]

    # Determina tamanho da série
    length = None
    for series in [atividade, passos, duracao_min]:
        if series is not None:
            length = len(series)
            break

    if length is None:
        raise ValueError("Ao menos uma das séries deve ser fornecida")

    # Inicializa com False
    is_pract = pd.Series([False] * length)

    # Verifica atividade esportiva
    if atividade is not None:
        pattern = "|".join(sport_activities)
        is_pract |= atividade.str.contains(pattern, case=False, na=False)

    # Verifica passos
    if passos is not None:
        is_pract |= passos >= min_passos

    # Verifica duração
    if duracao_min is not None:
        is_pract |= duracao_min >= min_duracao

    return is_pract


def parse_datetime_column(
    series: pd.Series, utc: bool = True, format: Optional[str] = None
) -> pd.Series:
    """
    Converte uma série para datetime com tratamento de erros.

    Args:
        series: Série a ser convertida
        utc: Se True, converte para UTC
        format: Formato específico do datetime (opcional)

    Returns:
        Série convertida para datetime
    """
    try:
        if format:
            result = pd.to_datetime(series, format=format, errors="coerce")
        else:
            result = pd.to_datetime(series, errors="coerce")

        if utc:
            result = result.dt.tz_localize("UTC", ambiguous="NaT", nonexistent="NaT")

        return result
    except Exception as e:
        print(f"⚠️  Erro ao converter para datetime: {e}")
        return pd.Series([pd.NaT] * len(series))


def remove_outliers_iqr(
    df: pd.DataFrame, column: str, factor: float = 1.5
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Remove outliers usando o método IQR (Interquartile Range).

    Args:
        df: DataFrame
        column: Nome da coluna para detectar outliers
        factor: Fator multiplicador do IQR (default: 1.5)

    Returns:
        Tupla (df_sem_outliers, df_outliers)
    """
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - factor * IQR
    upper_bound = Q3 + factor * IQR

    mask_ok = (df[column] >= lower_bound) & (df[column] <= upper_bound)
    df_clean = df[mask_ok].copy()
    df_outliers = df[~mask_ok].copy()

    if len(df_outliers) > 0:
        print(f"⚠️  Removidos {len(df_outliers)} outliers em '{column}' (IQR method)")

    return df_clean, df_outliers


if __name__ == "__main__":
    # Testes básicos
    print("✓ Módulo utils carregado com sucesso")

    # Teste safe_div
    assert safe_div(10, 2) == 5.0
    assert np.isnan(safe_div(10, 0))
    assert safe_div(10, 0, default=0) == 0

    # Teste bin_ages
    ages = pd.Series([15, 25, 35, 45, 55, 65])
    faixas = bin_ages(ages)
    assert len(faixas) == 6
    assert faixas.dtype.name == "category"

    # Teste calculate_imc
    imc = calculate_imc(70, 170)
    assert 24 < imc < 25

    print("✓ Testes básicos passaram")

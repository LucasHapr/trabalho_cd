"""
Módulo de I/O para leitura e escrita de dados.

Este módulo fornece funções para carregar e salvar dados em diferentes formatos
(CSV, Parquet, JSON), com tratamento de erros e logging.
"""

import json
from pathlib import Path
from typing import Optional, Union

import pandas as pd


def read_csv(
    filepath: Union[str, Path],
    encoding: str = "utf-8",
    separator: str = ",",
    parse_dates: Optional[list] = None,
    **kwargs,
) -> pd.DataFrame:
    """
    Lê um arquivo CSV e retorna um DataFrame.

    Args:
        filepath: Caminho do arquivo CSV
        encoding: Codificação do arquivo
        separator: Separador de colunas
        parse_dates: Lista de colunas para parsear como datas
        **kwargs: Argumentos adicionais para pd.read_csv

    Returns:
        DataFrame com os dados lidos

    Raises:
        FileNotFoundError: Se o arquivo não existir
        pd.errors.ParserError: Se houver erro ao parsear o CSV
    """
    filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")

    print(f"📖 Lendo CSV: {filepath}")

    try:
        df = pd.read_csv(
            filepath, encoding=encoding, sep=separator, parse_dates=parse_dates, **kwargs
        )
        print(f"✓ {len(df)} linhas, {len(df.columns)} colunas carregadas")
        return df
    except Exception as e:
        print(f"✗ Erro ao ler CSV: {e}")
        raise


def read_parquet(filepath: Union[str, Path], **kwargs) -> pd.DataFrame:
    """
    Lê um arquivo Parquet e retorna um DataFrame.

    Args:
        filepath: Caminho do arquivo Parquet
        **kwargs: Argumentos adicionais para pd.read_parquet

    Returns:
        DataFrame com os dados lidos

    Raises:
        FileNotFoundError: Se o arquivo não existir
    """
    filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")

    print(f"📖 Lendo Parquet: {filepath}")

    try:
        df = pd.read_parquet(filepath, engine="pyarrow", **kwargs)
        print(f"✓ {len(df)} linhas, {len(df.columns)} colunas carregadas")
        return df
    except Exception as e:
        print(f"✗ Erro ao ler Parquet: {e}")
        raise


def read_json(filepath: Union[str, Path], orient: str = "records", **kwargs) -> pd.DataFrame:
    """
    Lê um arquivo JSON e retorna um DataFrame.

    Args:
        filepath: Caminho do arquivo JSON
        orient: Formato do JSON ('records', 'index', 'columns', etc.)
        **kwargs: Argumentos adicionais para pd.read_json

    Returns:
        DataFrame com os dados lidos

    Raises:
        FileNotFoundError: Se o arquivo não existir
        json.JSONDecodeError: Se houver erro ao decodificar o JSON
    """
    filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")

    print(f"📖 Lendo JSON: {filepath}")

    try:
        df = pd.read_json(filepath, orient=orient, **kwargs)
        print(f"✓ {len(df)} linhas, {len(df.columns)} colunas carregadas")
        return df
    except Exception as e:
        print(f"✗ Erro ao ler JSON: {e}")
        raise


def save_parquet(
    df: pd.DataFrame,
    filepath: Union[str, Path],
    compression: str = "snappy",
    index: bool = False,
    **kwargs,
) -> None:
    """
    Salva um DataFrame como arquivo Parquet.

    Args:
        df: DataFrame a ser salvo
        filepath: Caminho do arquivo de saída
        compression: Algoritmo de compressão ('snappy', 'gzip', 'brotli', None)
        index: Se True, salva o índice
        **kwargs: Argumentos adicionais para df.to_parquet
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    print(f"💾 Salvando Parquet: {filepath}")

    try:
        df.to_parquet(filepath, engine="pyarrow", compression=compression, index=index, **kwargs)
        file_size = filepath.stat().st_size / (1024 * 1024)  # MB
        print(f"✓ {len(df)} linhas salvas ({file_size:.2f} MB)")
    except Exception as e:
        print(f"✗ Erro ao salvar Parquet: {e}")
        raise


def save_csv(
    df: pd.DataFrame,
    filepath: Union[str, Path],
    encoding: str = "utf-8",
    index: bool = False,
    **kwargs,
) -> None:
    """
    Salva um DataFrame como arquivo CSV.

    Args:
        df: DataFrame a ser salvo
        filepath: Caminho do arquivo de saída
        encoding: Codificação do arquivo
        index: Se True, salva o índice
        **kwargs: Argumentos adicionais para df.to_csv
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    print(f"💾 Salvando CSV: {filepath}")

    try:
        df.to_csv(filepath, encoding=encoding, index=index, **kwargs)
        file_size = filepath.stat().st_size / (1024 * 1024)  # MB
        print(f"✓ {len(df)} linhas salvas ({file_size:.2f} MB)")
    except Exception as e:
        print(f"✗ Erro ao salvar CSV: {e}")
        raise


def save_json(
    df: pd.DataFrame, filepath: Union[str, Path], orient: str = "records", indent: int = 2, **kwargs
) -> None:
    """
    Salva um DataFrame como arquivo JSON.

    Args:
        df: DataFrame a ser salvo
        filepath: Caminho do arquivo de saída
        orient: Formato do JSON ('records', 'index', 'columns', etc.)
        indent: Número de espaços para indentação
        **kwargs: Argumentos adicionais para df.to_json
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    print(f"💾 Salvando JSON: {filepath}")

    try:
        df.to_json(filepath, orient=orient, indent=indent, force_ascii=False, **kwargs)
        file_size = filepath.stat().st_size / (1024 * 1024)  # MB
        print(f"✓ {len(df)} linhas salvas ({file_size:.2f} MB)")
    except Exception as e:
        print(f"✗ Erro ao salvar JSON: {e}")
        raise


def load_data(
    filepath: Union[str, Path], format: Optional[str] = None, **kwargs
) -> pd.DataFrame:
    """
    Carrega dados de um arquivo, detectando automaticamente o formato.

    Args:
        filepath: Caminho do arquivo
        format: Formato do arquivo ('csv', 'parquet', 'json'). Se None, detecta pela extensão
        **kwargs: Argumentos adicionais para as funções de leitura específicas

    Returns:
        DataFrame com os dados lidos

    Raises:
        ValueError: Se o formato não for suportado
    """
    filepath = Path(filepath)

    if format is None:
        format = filepath.suffix.lower().lstrip(".")

    format_readers = {
        "csv": read_csv,
        "parquet": read_parquet,
        "pq": read_parquet,
        "json": read_json,
    }

    if format not in format_readers:
        raise ValueError(
            f"Formato '{format}' não suportado. Use: {list(format_readers.keys())}"
        )

    return format_readers[format](filepath, **kwargs)


def save_data(
    df: pd.DataFrame, filepath: Union[str, Path], format: Optional[str] = None, **kwargs
) -> None:
    """
    Salva um DataFrame em um arquivo, detectando automaticamente o formato.

    Args:
        df: DataFrame a ser salvo
        filepath: Caminho do arquivo de saída
        format: Formato do arquivo ('csv', 'parquet', 'json'). Se None, detecta pela extensão
        **kwargs: Argumentos adicionais para as funções de escrita específicas

    Raises:
        ValueError: Se o formato não for suportado
    """
    filepath = Path(filepath)

    if format is None:
        format = filepath.suffix.lower().lstrip(".")

    format_writers = {
        "csv": save_csv,
        "parquet": save_parquet,
        "pq": save_parquet,
        "json": save_json,
    }

    if format not in format_writers:
        raise ValueError(
            f"Formato '{format}' não suportado. Use: {list(format_writers.keys())}"
        )

    format_writers[format](df, filepath, **kwargs)


if __name__ == "__main__":
    # Teste básico
    print("✓ Módulo dataio carregado com sucesso")
    print(f"  Formatos suportados para leitura: csv, parquet, json")
    print(f"  Formatos suportados para escrita: csv, parquet, json")

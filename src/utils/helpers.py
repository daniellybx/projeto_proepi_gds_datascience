"""
Funções auxiliares e utilitários gerais para o projeto Guardiões da Saúde - ProEpi
"""

import pandas as pd
import numpy as np
from typing import Any, Dict, List, Optional, Union, Tuple
from pathlib import Path
import json
import pickle
import joblib
from datetime import datetime, timedelta
import warnings
from functools import wraps
import time


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Divisão segura que evita divisão por zero
    
    Args:
        numerator: Numerador
        denominator: Denominador
        default: Valor padrão se denominador for zero
        
    Returns:
        Resultado da divisão ou valor padrão
    """
    if denominator == 0 or pd.isna(denominator):
        return default
    return numerator / denominator


def calculate_incidence_rate(cases: int, population: int, multiplier: int = 100000) -> float:
    """
    Calcula taxa de incidência padronizada
    
    Args:
        cases: Número de casos
        population: População total
        multiplier: Multiplicador para padronização (default: 100.000)
        
    Returns:
        Taxa de incidência por 100.000 habitantes
    """
    return safe_divide(cases * multiplier, population)


def detect_outliers_iqr(data: pd.Series, multiplier: float = 1.5) -> pd.Series:
    """
    Detecta outliers usando o método IQR
    
    Args:
        data: Série de dados
        multiplier: Multiplicador do IQR (default: 1.5)
        
    Returns:
        Série booleana indicando outliers
    """
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - multiplier * IQR
    upper_bound = Q3 + multiplier * IQR
    
    return (data < lower_bound) | (data > upper_bound)


def detect_outliers_zscore(data: pd.Series, threshold: float = 3.0) -> pd.Series:
    """
    Detecta outliers usando Z-score
    
    Args:
        data: Série de dados
        threshold: Limite do Z-score (default: 3.0)
        
    Returns:
        Série booleana indicando outliers
    """
    z_scores = np.abs((data - data.mean()) / data.std())
    return z_scores > threshold


def save_object(obj: Any, filepath: Union[str, Path], method: str = 'auto') -> None:
    """
    Salva objeto em arquivo usando diferentes métodos
    
    Args:
        obj: Objeto para salvar
        filepath: Caminho do arquivo
        method: Método de serialização ('pickle', 'joblib', 'json', 'auto')
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    if method == 'auto':
        if filepath.suffix == '.pkl':
            method = 'pickle'
        elif filepath.suffix == '.joblib':
            method = 'joblib'
        elif filepath.suffix == '.json':
            method = 'json'
        else:
            method = 'pickle'
    
    if method == 'pickle':
        with open(filepath, 'wb') as f:
            pickle.dump(obj, f)
    elif method == 'joblib':
        joblib.dump(obj, filepath)
    elif method == 'json':
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(obj, f, default=str, ensure_ascii=False, indent=2)
    else:
        raise ValueError(f"Método não suportado: {method}")


def load_object(filepath: Union[str, Path], method: str = 'auto') -> Any:
    """
    Carrega objeto de arquivo usando diferentes métodos
    
    Args:
        filepath: Caminho do arquivo
        method: Método de deserialização ('pickle', 'joblib', 'json', 'auto')
        
    Returns:
        Objeto carregado
    """
    filepath = Path(filepath)
    
    if method == 'auto':
        if filepath.suffix == '.pkl':
            method = 'pickle'
        elif filepath.suffix == '.joblib':
            method = 'joblib'
        elif filepath.suffix == '.json':
            method = 'json'
        else:
            method = 'pickle'
    
    if method == 'pickle':
        with open(filepath, 'rb') as f:
            return pickle.load(f)
    elif method == 'joblib':
        return joblib.load(filepath)
    elif method == 'json':
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        raise ValueError(f"Método não suportado: {method}")


def memory_usage_mb(df: pd.DataFrame) -> float:
    """
    Calcula uso de memória de um DataFrame em MB
    
    Args:
        df: DataFrame para analisar
        
    Returns:
        Uso de memória em MB
    """
    return df.memory_usage(deep=True).sum() / 1024**2


def optimize_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Otimiza tipos de dados de um DataFrame para reduzir uso de memória
    
    Args:
        df: DataFrame para otimizar
        
    Returns:
        DataFrame otimizado
    """
    df_optimized = df.copy()
    
    for col in df_optimized.columns:
        col_type = df_optimized[col].dtype
        
        if col_type != 'object':
            c_min = df_optimized[col].min()
            c_max = df_optimized[col].max()
            
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df_optimized[col] = df_optimized[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df_optimized[col] = df_optimized[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df_optimized[col] = df_optimized[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df_optimized[col] = df_optimized[col].astype(np.int64)
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df_optimized[col] = df_optimized[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df_optimized[col] = df_optimized[col].astype(np.float32)
                else:
                    df_optimized[col] = df_optimized[col].astype(np.float64)
        else:
            df_optimized[col] = df_optimized[col].astype('category')
    
    return df_optimized


def timer(func):
    """
    Decorator para medir tempo de execução de funções
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} executado em {end_time - start_time:.2f} segundos")
        return result
    return wrapper


def suppress_warnings(func):
    """
    Decorator para suprimir warnings durante execução
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return func(*args, **kwargs)
    return wrapper


def validate_dataframe(df: pd.DataFrame, required_columns: List[str] = None) -> bool:
    """
    Valida se DataFrame tem estrutura esperada
    
    Args:
        df: DataFrame para validar
        required_columns: Lista de colunas obrigatórias
        
    Returns:
        True se válido, False caso contrário
    """
    if df.empty:
        print("DataFrame está vazio")
        return False
    
    if required_columns:
        missing_columns = set(required_columns) - set(df.columns)
        if missing_columns:
            print(f"Colunas obrigatórias ausentes: {missing_columns}")
            return False
    
    return True


def get_date_range(start_date: str, end_date: str, freq: str = 'D') -> pd.DatetimeIndex:
    """
    Gera range de datas
    
    Args:
        start_date: Data inicial (YYYY-MM-DD)
        end_date: Data final (YYYY-MM-DD)
        freq: Frequência ('D', 'W', 'M', 'Y')
        
    Returns:
        Range de datas
    """
    return pd.date_range(start=start_date, end=end_date, freq=freq)


def calculate_rolling_stats(data: pd.Series, window: int, stats: List[str] = None) -> pd.DataFrame:
    """
    Calcula estatísticas móveis
    
    Args:
        data: Série de dados
        window: Janela móvel
        stats: Lista de estatísticas ['mean', 'std', 'min', 'max', 'median']
        
    Returns:
        DataFrame com estatísticas móveis
    """
    if stats is None:
        stats = ['mean', 'std', 'min', 'max']
    
    result = pd.DataFrame(index=data.index)
    
    for stat in stats:
        if stat == 'mean':
            result[f'rolling_{stat}_{window}'] = data.rolling(window=window).mean()
        elif stat == 'std':
            result[f'rolling_{stat}_{window}'] = data.rolling(window=window).std()
        elif stat == 'min':
            result[f'rolling_{stat}_{window}'] = data.rolling(window=window).min()
        elif stat == 'max':
            result[f'rolling_{stat}_{window}'] = data.rolling(window=window).max()
        elif stat == 'median':
            result[f'rolling_{stat}_{window}'] = data.rolling(window=window).median()
    
    return result

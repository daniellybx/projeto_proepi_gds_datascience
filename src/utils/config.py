"""
Configurações do projeto Guardiões da Saúde - ProEpi
"""

import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()


class Config:
    """
    Classe de configuração centralizada do projeto
    
    Desenvolvido por: Danielly Xavier
    Email: danielly.xavier@outlook.com
    """
    
    # Configurações de Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    # Configurações de Dados
    DATA_PATH = Path(os.getenv("DATA_PATH", "data/raw"))
    PROCESSED_DATA_PATH = Path(os.getenv("PROCESSED_DATA_PATH", "data/processed"))
    EXTERNAL_DATA_PATH = Path(os.getenv("EXTERNAL_DATA_PATH", "data/external"))
    
    # Configurações de Modelos
    MODEL_PATH = Path(os.getenv("MODEL_PATH", "models"))
    RANDOM_STATE = int(os.getenv("RANDOM_STATE", "42"))
    
    # Configurações de Visualização
    PLOT_STYLE = os.getenv("PLOT_STYLE", "seaborn")
    FIGURE_SIZE = eval(os.getenv("FIGURE_SIZE", "(12, 8)"))
    DPI = int(os.getenv("DPI", "300"))
    
    # Configurações de Análise
    CONFIDENCE_INTERVAL = float(os.getenv("CONFIDENCE_INTERVAL", "0.95"))
    ANOMALY_THRESHOLD = float(os.getenv("ANOMALY_THRESHOLD", "2.0"))
    
    # Configurações de Performance
    N_JOBS = int(os.getenv("N_JOBS", "-1"))
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "10000"))
    
    @classmethod
    def create_directories(cls) -> None:
        """
        Cria os diretórios necessários do projeto
        """
        directories = [
            cls.DATA_PATH,
            cls.PROCESSED_DATA_PATH,
            cls.EXTERNAL_DATA_PATH,
            cls.MODEL_PATH,
            Path("reports"),
            Path("logs")
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def get_config_dict(cls) -> Dict[str, Any]:
        """
        Retorna todas as configurações como dicionário
        """
        return {
            "log_level": cls.LOG_LEVEL,
            "log_format": cls.LOG_FORMAT,
            "data_path": str(cls.DATA_PATH),
            "processed_data_path": str(cls.PROCESSED_DATA_PATH),
            "external_data_path": str(cls.EXTERNAL_DATA_PATH),
            "model_path": str(cls.MODEL_PATH),
            "random_state": cls.RANDOM_STATE,
            "plot_style": cls.PLOT_STYLE,
            "figure_size": cls.FIGURE_SIZE,
            "dpi": cls.DPI,
            "confidence_interval": cls.CONFIDENCE_INTERVAL,
            "anomaly_threshold": cls.ANOMALY_THRESHOLD,
            "n_jobs": cls.N_JOBS,
            "chunk_size": cls.CHUNK_SIZE
        }

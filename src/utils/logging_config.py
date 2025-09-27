"""
Configuração de logging para o projeto Guardiões da Saúde - ProEpi
"""

import logging
import sys
from pathlib import Path
from typing import Optional
from .config import Config


def setup_logging(
    log_level: Optional[str] = None,
    log_file: Optional[str] = None,
    log_format: Optional[str] = None
) -> logging.Logger:
    """
    Configura o sistema de logging do projeto
    
    Args:
        log_level: Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Arquivo para salvar logs (opcional)
        log_format: Formato das mensagens de log
        
    Returns:
        Logger configurado
    """
    # Usa configurações padrão se não especificadas
    log_level = log_level or Config.LOG_LEVEL
    log_format = log_format or Config.LOG_FORMAT
    
    # Cria diretório de logs se necessário
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configura o logger principal
    logger = logging.getLogger("proepi_gds")
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Remove handlers existentes para evitar duplicação
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Formatter
    formatter = logging.Formatter(log_format)
    
    # Handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level.upper()))
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Handler para arquivo (se especificado)
    if log_file:
        file_handler = logging.FileHandler(log_dir / log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)  # Arquivo sempre DEBUG
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    # Configura loggers de bibliotecas externas
    _configure_external_loggers()
    
    logger.info(f"Logging configurado - Nível: {log_level}")
    return logger


def _configure_external_loggers():
    """
    Configura níveis de log para bibliotecas externas
    """
    # Reduz verbosidade de bibliotecas específicas
    external_loggers = {
        'matplotlib': 'WARNING',
        'PIL': 'WARNING',
        'urllib3': 'WARNING',
        'requests': 'WARNING',
        'tensorflow': 'WARNING',
        'keras': 'WARNING',
        'prophet': 'WARNING',
        'xgboost': 'WARNING'
    }
    
    for logger_name, level in external_loggers.items():
        logging.getLogger(logger_name).setLevel(getattr(logging, level))


def get_logger(name: str) -> logging.Logger:
    """
    Obtém um logger específico para um módulo
    
    Args:
        name: Nome do módulo (geralmente __name__)
        
    Returns:
        Logger configurado
    """
    return logging.getLogger(f"proepi_gds.{name}")


class LoggerMixin:
    """
    Mixin para adicionar funcionalidade de logging a classes
    """
    
    @property
    def logger(self) -> logging.Logger:
        """Retorna o logger para a classe"""
        return get_logger(self.__class__.__module__ + "." + self.__class__.__name__)

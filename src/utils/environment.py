"""
Configuração e validação do ambiente para o projeto Guardiões da Saúde - ProEpi
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
import subprocess
import importlib
from .config import Config
from .logging_config import get_logger

logger = get_logger(__name__)


class EnvironmentValidator:
    """
    Validador do ambiente de desenvolvimento
    """
    
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def validate_python_version(self, min_version: tuple = (3, 8)) -> bool:
        """
        Valida versão do Python
        
        Args:
            min_version: Versão mínima requerida (major, minor)
            
        Returns:
            True se versão é adequada
        """
        current_version = sys.version_info[:2]
        if current_version < min_version:
            self.errors.append(
                f"Python {min_version[0]}.{min_version[1]}+ requerido. "
                f"Versão atual: {current_version[0]}.{current_version[1]}"
            )
            return False
        
        logger.info(f"Python {current_version[0]}.{current_version[1]} - OK")
        return True
    
    def validate_dependencies(self, requirements_file: str = "requirements.txt") -> bool:
        """
        Valida se todas as dependências estão instaladas
        
        Args:
            requirements_file: Arquivo de requirements
            
        Returns:
            True se todas as dependências estão instaladas
        """
        if not Path(requirements_file).exists():
            self.warnings.append(f"Arquivo {requirements_file} não encontrado")
            return True
        
        missing_packages = []
        
        with open(requirements_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    package_name = line.split('>=')[0].split('==')[0].split('[')[0]
                    try:
                        importlib.import_module(package_name.replace('-', '_'))
                    except ImportError:
                        missing_packages.append(package_name)
        
        if missing_packages:
            self.errors.append(f"Pacotes não instalados: {', '.join(missing_packages)}")
            return False
        
        logger.info("Todas as dependências estão instaladas - OK")
        return True
    
    def validate_directories(self) -> bool:
        """
        Valida se diretórios necessários existem
        
        Returns:
            True se todos os diretórios existem
        """
        required_dirs = [
            Config.DATA_PATH,
            Config.PROCESSED_DATA_PATH,
            Config.EXTERNAL_DATA_PATH,
            Config.MODEL_PATH,
            Path("logs"),
            Path("reports")
        ]
        
        missing_dirs = []
        for directory in required_dirs:
            if not directory.exists():
                missing_dirs.append(str(directory))
                directory.mkdir(parents=True, exist_ok=True)
                logger.info(f"Diretório criado: {directory}")
        
        if missing_dirs:
            self.warnings.append(f"Diretórios criados: {', '.join(missing_dirs)}")
        
        logger.info("Estrutura de diretórios - OK")
        return True
    
    def validate_data_access(self) -> bool:
        """
        Valida acesso aos dados
        
        Returns:
            True se acesso aos dados está OK
        """
        data_path = Config.DATA_PATH
        
        if not data_path.exists():
            self.warnings.append(f"Diretório de dados não existe: {data_path}")
            return True
        
        # Verifica se há arquivos de dados
        data_files = list(data_path.glob("**/*"))
        data_files = [f for f in data_files if f.is_file() and not f.name.startswith('.')]
        
        if not data_files:
            self.warnings.append("Nenhum arquivo de dados encontrado em data/raw/")
        else:
            logger.info(f"Encontrados {len(data_files)} arquivos de dados")
        
        return True
    
    def validate_environment_variables(self) -> bool:
        """
        Valida variáveis de ambiente importantes
        
        Returns:
            True se variáveis estão configuradas corretamente
        """
        # Verifica se arquivo .env existe
        env_file = Path(".env")
        if not env_file.exists():
            self.warnings.append("Arquivo .env não encontrado. Usando configurações padrão.")
        
        # Valida configurações críticas
        if Config.RANDOM_STATE is None:
            self.warnings.append("RANDOM_STATE não definido. Usando valor padrão.")
        
        logger.info("Variáveis de ambiente - OK")
        return True
    
    def run_all_checks(self) -> Dict[str, Any]:
        """
        Executa todas as validações
        
        Returns:
            Dicionário com resultados das validações
        """
        logger.info("Iniciando validação do ambiente...")
        
        checks = {
            'python_version': self.validate_python_version(),
            'dependencies': self.validate_dependencies(),
            'directories': self.validate_directories(),
            'data_access': self.validate_data_access(),
            'environment_variables': self.validate_environment_variables()
        }
        
        all_passed = all(checks.values())
        
        result = {
            'all_passed': all_passed,
            'checks': checks,
            'errors': self.errors,
            'warnings': self.warnings
        }
        
        if all_passed:
            logger.info("✅ Validação do ambiente concluída com sucesso!")
        else:
            logger.error("❌ Validação do ambiente falhou!")
            for error in self.errors:
                logger.error(f"  - {error}")
        
        for warning in self.warnings:
            logger.warning(f"  ⚠️  {warning}")
        
        return result


def setup_environment(force: bool = False) -> bool:
    """
    Configura o ambiente do projeto
    
    Args:
        force: Se True, força configuração mesmo com erros
        
    Returns:
        True se configuração foi bem-sucedida
    """
    logger.info("Configurando ambiente do projeto...")
    
    # Cria diretórios necessários
    Config.create_directories()
    
    # Valida ambiente
    validator = EnvironmentValidator()
    result = validator.run_all_checks()
    
    if result['all_passed'] or force:
        logger.info("Ambiente configurado com sucesso!")
        return True
    else:
        logger.error("Falha na configuração do ambiente")
        return False


def check_gpu_availability() -> Dict[str, Any]:
    """
    Verifica disponibilidade de GPU para TensorFlow
    
    Returns:
        Dicionário com informações sobre GPU
    """
    gpu_info = {
        'available': False,
        'devices': [],
        'tensorflow_gpu': False
    }
    
    try:
        import tensorflow as tf
        
        # Verifica se TensorFlow detecta GPU
        gpu_devices = tf.config.list_physical_devices('GPU')
        gpu_info['devices'] = [device.name for device in gpu_devices]
        gpu_info['available'] = len(gpu_devices) > 0
        gpu_info['tensorflow_gpu'] = tf.test.is_built_with_cuda()
        
        if gpu_info['available']:
            logger.info(f"GPU disponível: {gpu_info['devices']}")
        else:
            logger.info("GPU não disponível - usando CPU")
            
    except ImportError:
        logger.warning("TensorFlow não instalado - não é possível verificar GPU")
    except Exception as e:
        logger.warning(f"Erro ao verificar GPU: {e}")
    
    return gpu_info


def get_system_info() -> Dict[str, Any]:
    """
    Coleta informações do sistema
    
    Returns:
        Dicionário com informações do sistema
    """
    import platform
    import psutil
    
    info = {
        'python_version': sys.version,
        'platform': platform.platform(),
        'processor': platform.processor(),
        'cpu_count': psutil.cpu_count(),
        'memory_total': psutil.virtual_memory().total,
        'memory_available': psutil.virtual_memory().available,
        'disk_usage': psutil.disk_usage('/').percent if os.name != 'nt' else psutil.disk_usage('C:').percent
    }
    
    return info

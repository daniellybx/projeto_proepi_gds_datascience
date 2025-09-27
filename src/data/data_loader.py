"""
Módulo para carregamento de dados do projeto Guardiões da Saúde
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, Union, Dict, Any
import logging

logger = logging.getLogger(__name__)


class DataLoader:
    """
    Classe para carregamento de dados do aplicativo Guardiões da Saúde
    """
    
    def __init__(self, data_path: Union[str, Path] = "data/raw"):
        """
        Inicializa o carregador de dados
        
        Args:
            data_path: Caminho para o diretório de dados
        """
        self.data_path = Path(data_path)
        self.data_path.mkdir(parents=True, exist_ok=True)
        
    def load_symptoms_data(self, filename: str = "gds-unb-ano-2024-extractionAt-20250903.csv") -> pd.DataFrame:
        """
        Carrega dados de sintomas do GoH
        
        Args:
            filename: Nome do arquivo de dados
            
        Returns:
            DataFrame com os dados de sintomas
        """
        file_path = self.data_path / filename
        
        if not file_path.exists():
            logger.warning(f"Arquivo {file_path} não encontrado. Retornando DataFrame vazio.")
            return pd.DataFrame()
            
        try:
            # Carrega dados sem cabeçalho
            df = pd.read_csv(file_path, header=None)
            
            # Define nomes das colunas baseado no dicionário de dados
            column_names = [
                'report_id', 'user_id', 'report_bad_since', 'report_contact_with_symptom',
                'report_created_at', 'report_latitude', 'report_longitude', 'report_symptoms',
                'symptom_1', 'symptom_2', 'symptom_3', 'symptom_4', 'symptom_5', 'symptom_6',
                'symptom_7', 'syndrome_id', 'data_extracted_at'
            ]
            
            # Ajusta o número de colunas se necessário
            if len(df.columns) != len(column_names):
                logger.warning(f"Número de colunas ({len(df.columns)}) diferente do esperado ({len(column_names)})")
                # Usa nomes genéricos se não bater
                df.columns = [f'col_{i}' for i in range(len(df.columns))]
            else:
                df.columns = column_names
            
            logger.info(f"Dados carregados com sucesso: {len(df)} registros, {len(df.columns)} colunas")
            return df
            
        except Exception as e:
            logger.error(f"Erro ao carregar dados: {e}")
            raise
    
    def load_user_data(self, filename: str = "usuarios_goh.csv") -> pd.DataFrame:
        """
        Carrega dados de usuários do GoH
        
        Args:
            filename: Nome do arquivo de dados de usuários
            
        Returns:
            DataFrame com os dados de usuários
        """
        file_path = self.data_path / filename
        
        if not file_path.exists():
            logger.warning(f"Arquivo {file_path} não encontrado. Retornando DataFrame vazio.")
            return pd.DataFrame()
            
        try:
            df = pd.read_csv(file_path)
            logger.info(f"Dados de usuários carregados: {len(df)} registros")
            return df
        except Exception as e:
            logger.error(f"Erro ao carregar dados de usuários: {e}")
            raise
    
    def load_metadata(self, filename: str = "metadata.json") -> Dict[str, Any]:
        """
        Carrega metadados do projeto
        
        Args:
            filename: Nome do arquivo de metadados
            
        Returns:
            Dicionário com metadados
        """
        import json
        
        file_path = self.data_path / filename
        
        if not file_path.exists():
            logger.warning(f"Arquivo de metadados {file_path} não encontrado.")
            return {}
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            logger.info("Metadados carregados com sucesso")
            return metadata
        except Exception as e:
            logger.error(f"Erro ao carregar metadados: {e}")
            return {}
    
    def save_processed_data(self, df: pd.DataFrame, filename: str, 
                           subfolder: str = "processed") -> None:
        """
        Salva dados processados
        
        Args:
            df: DataFrame para salvar
            filename: Nome do arquivo
            subfolder: Subpasta onde salvar (default: processed)
        """
        save_path = self.data_path.parent / subfolder
        save_path.mkdir(parents=True, exist_ok=True)
        
        file_path = save_path / filename
        
        try:
            if filename.endswith('.csv'):
                df.to_csv(file_path, index=False)
            elif filename.endswith('.parquet'):
                df.to_parquet(file_path, index=False)
            elif filename.endswith('.xlsx'):
                df.to_excel(file_path, index=False)
            else:
                raise ValueError(f"Formato de arquivo não suportado: {filename}")
                
            logger.info(f"Dados salvos em: {file_path}")
        except Exception as e:
            logger.error(f"Erro ao salvar dados: {e}")
            raise

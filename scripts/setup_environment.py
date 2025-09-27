#!/usr/bin/env python3
"""
Script de configuração do ambiente para o projeto Guardiões da Saúde - ProEpi
"""

import sys
import os
from pathlib import Path

# Adiciona o diretório raiz ao path para importar módulos
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.utils.environment import setup_environment, check_gpu_availability, get_system_info
from src.utils.logging_config import setup_logging
from src.utils.config import Config


def main():
    """
    Função principal para configuração do ambiente
    """
    print("🏥 Projeto Guardiões da Saúde - ProEpi")
    print("👩‍💻 Desenvolvido por: Danielly Xavier")
    print("📧 Contato: danielly.xavier@outlook.com")
    print("=" * 50)
    print("Configurando ambiente de desenvolvimento...")
    print()
    
    # Configura logging
    logger = setup_logging()
    
    # Mostra informações do sistema
    print("📊 Informações do Sistema:")
    system_info = get_system_info()
    print(f"  Python: {system_info['python_version'].split()[0]}")
    print(f"  Plataforma: {system_info['platform']}")
    print(f"  CPU: {system_info['cpu_count']} cores")
    print(f"  Memória: {system_info['memory_total'] // (1024**3)} GB")
    print()
    
    # Verifica GPU
    print("🖥️  Verificando GPU:")
    gpu_info = check_gpu_availability()
    if gpu_info['available']:
        print(f"  ✅ GPU disponível: {', '.join(gpu_info['devices'])}")
    else:
        print("  ⚠️  GPU não disponível - usando CPU")
    print()
    
    # Configura ambiente
    print("⚙️  Configurando ambiente:")
    success = setup_environment()
    
    if success:
        print("✅ Ambiente configurado com sucesso!")
        print()
        print("📁 Estrutura de diretórios criada:")
        print(f"  - Dados brutos: {Config.DATA_PATH}")
        print(f"  - Dados processados: {Config.PROCESSED_DATA_PATH}")
        print(f"  - Dados externos: {Config.EXTERNAL_DATA_PATH}")
        print(f"  - Modelos: {Config.MODEL_PATH}")
        print(f"  - Logs: logs/")
        print(f"  - Relatórios: reports/")
        print()
        print("🚀 Pronto para começar o desenvolvimento!")
        print()
        print("Próximos passos:")
        print("1. Adicione seus dados em data/raw/")
        print("2. Execute os notebooks em notebooks/")
        print("3. Use os módulos em src/ para suas análises")
        
    else:
        print("❌ Falha na configuração do ambiente!")
        print("Verifique os erros acima e tente novamente.")
        sys.exit(1)


if __name__ == "__main__":
    main()

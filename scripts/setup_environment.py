#!/usr/bin/env python3
"""
Script de configuração do ambiente para o projeto Guardiões da Saúde - ProEpi
"""

import argparse
import sys
import os
import shutil
import subprocess
from pathlib import Path

# Adiciona o diretório raiz ao path para importar módulos
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def _run_command(command: list[str], cwd: Path, env: dict | None = None) -> bool:
    """Executa um comando e retorna True em caso de sucesso."""
    try:
        subprocess.run(command, cwd=str(cwd), env=env, check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def _resolve_venv_python(venv_path: Path) -> Path:
    """Resolve o executável Python dentro do venv para Linux/macOS/Windows."""
    if os.name == "nt":
        return venv_path / "Scripts" / "python.exe"
    return venv_path / "bin" / "python"


def _create_virtualenv(venv_path: Path, use_uv: bool) -> tuple[bool, str]:
    """
    Cria um ambiente virtual.

    Retorna:
        (success, manager_name) onde manager_name é 'uv' ou 'pip'
    """
    uv_binary = shutil.which("uv")
    if use_uv and uv_binary:
        command = [uv_binary, "venv", str(venv_path)]
        if _run_command(command, cwd=project_root):
            return True, "uv"
        return False, "uv"

    command = [sys.executable, "-m", "venv", str(venv_path)]
    if _run_command(command, cwd=project_root):
        return True, "pip"
    return False, "pip"


def _install_dependencies(venv_python: Path, requirements_file: Path, manager: str) -> bool:
    """Instala dependências usando uv (preferencial) ou pip."""
    if manager == "uv":
        uv_binary = shutil.which("uv")
        if not uv_binary:
            return False
        command = [
            uv_binary,
            "pip",
            "install",
            "--python",
            str(venv_python),
            "-r",
            str(requirements_file),
        ]
        return _run_command(command, cwd=project_root)

    command = [str(venv_python), "-m", "pip", "install", "-r", str(requirements_file)]
    return _run_command(command, cwd=project_root)


def _install_notebook_kernel(venv_python: Path, kernel_name: str, display_name: str, manager: str) -> bool:
    """Instala ipykernel/jupyter e registra kernel para notebooks."""
    if manager == "uv":
        uv_binary = shutil.which("uv")
        if not uv_binary:
            return False
        install_ok = _run_command(
            [uv_binary, "pip", "install", "--python", str(venv_python), "ipykernel", "jupyter"],
            cwd=project_root
        )
    else:
        install_ok = _run_command(
            [str(venv_python), "-m", "pip", "install", "ipykernel", "jupyter"],
            cwd=project_root
        )

    if not install_ok:
        return False

    return _run_command(
        [
            str(venv_python),
            "-m",
            "ipykernel",
            "install",
            "--user",
            "--name",
            kernel_name,
            "--display-name",
            display_name,
        ],
        cwd=project_root
    )


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Configura ambiente local do projeto Guardiões da Saúde - ProEpi."
    )
    parser.add_argument(
        "--venv-path",
        default=".venv",
        help="Caminho do ambiente virtual relativo à raiz do projeto (padrão: .venv).",
    )
    parser.add_argument(
        "--requirements-file",
        default="requirements.txt",
        help="Arquivo de dependências (padrão: requirements.txt).",
    )
    parser.add_argument(
        "--recreate-venv",
        action="store_true",
        help="Apaga o venv existente e recria do zero.",
    )
    parser.add_argument(
        "--skip-kernel",
        action="store_true",
        help="Não instala/register o kernel Jupyter.",
    )
    parser.add_argument(
        "--kernel-name",
        default="proepi-unico",
        help="Nome técnico do kernel Jupyter (padrão: proepi-unico).",
    )
    parser.add_argument(
        "--kernel-display-name",
        default="Python (.venv proepi)",
        help="Nome exibido no Jupyter/Cursor.",
    )
    parser.add_argument(
        "--no-uv",
        action="store_true",
        help="Força uso de python -m venv/pip sem uv.",
    )
    return parser.parse_args()


def main():
    """Função principal para configuração do ambiente."""
    args = _parse_args()

    from src.utils.environment import setup_environment, check_gpu_availability, get_system_info
    from src.utils.logging_config import setup_logging
    from src.utils.config import Config

    venv_path = (project_root / args.venv_path).resolve()
    requirements_path = (project_root / args.requirements_file).resolve()

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

    if not requirements_path.exists():
        print(f"❌ Arquivo de dependências não encontrado: {requirements_path}")
        sys.exit(1)

    if args.recreate_venv and venv_path.exists():
        print(f"🧹 Removendo ambiente anterior: {venv_path}")
        shutil.rmtree(venv_path)

    print("⚙️  Provisionando ambiente Python:")
    use_uv = not args.no_uv
    created, manager = _create_virtualenv(venv_path, use_uv=use_uv)
    if not created:
        print(f"❌ Não foi possível criar o ambiente virtual com {manager}.")
        sys.exit(1)

    venv_python = _resolve_venv_python(venv_path)
    if not venv_python.exists():
        print(f"❌ Python do ambiente não encontrado em: {venv_python}")
        sys.exit(1)

    print(f"  ✅ Ambiente criado em: {venv_path}")
    print(f"  ✅ Gerenciador: {manager}")

    print("📦 Instalando dependências do projeto...")
    deps_ok = _install_dependencies(venv_python, requirements_path, manager=manager)
    if not deps_ok:
        print("❌ Falha ao instalar dependências.")
        sys.exit(1)

    if not args.skip_kernel:
        print("📓 Instalando e registrando kernel Jupyter...")
        kernel_ok = _install_notebook_kernel(
            venv_python=venv_python,
            kernel_name=args.kernel_name,
            display_name=args.kernel_display_name,
            manager=manager,
        )
        if not kernel_ok:
            print("⚠️  Não foi possível registrar o kernel Jupyter.")
            print("   O ambiente foi criado, mas notebooks podem exigir ajuste manual de kernel.")
        else:
            print(f"  ✅ Kernel registrado: {args.kernel_display_name}")

    # Configura estrutura do projeto
    print()
    print("🗂️  Configurando estrutura do projeto:")
    success = setup_environment()

    if success:
        print("✅ Ambiente configurado com sucesso!")
        print()
        print("🔧 Como ativar o ambiente:")
        if os.name == "nt":
            print(f"  {venv_path}\\Scripts\\activate")
        else:
            print(f"  source \"{venv_path}/bin/activate\"")
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

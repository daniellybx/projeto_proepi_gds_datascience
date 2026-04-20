"""Define configuration objects for the agent diagnosis production pipeline.

This module centralizes local path and LLaMA/Ollama settings used by the
agent diagnosis application.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os

from src.utils.pathing import find_project_root


@dataclass
class LlamaConfig:
    """Store local LLaMA translation settings.

    Args:
        ollama_host (str): Ollama host URL.
        preferred_models (tuple[str, ...]): Model preference order.

    Returns:
        None: Dataclass instance with runtime settings.

    Example:
        >>> LlamaConfig.default()
    """

    ollama_host: str
    preferred_models: tuple[str, ...]

    @classmethod
    def default(cls) -> "LlamaConfig":
        """Create default local LLaMA configuration.

        Args:
            None

        Returns:
            LlamaConfig: Default translation configuration.

        Example:
            >>> cfg = LlamaConfig.default()
        """
        return cls(
            ollama_host=os.getenv("OLLAMA_HOST", "http://localhost:11434"),
            preferred_models=("llama3.2", "llama3.1", "llama3", "mistral", "phi3", "gemma", "llama2"),
        )


@dataclass
class AgentDiagnosisConfig:
    """Store pipeline paths and ranking thresholds for diagnosis generation.

    Args:
        root (Path): Project root directory.
        output_dir (Path): Destination directory for parquet outputs.
        primary_threshold (float): Minimum similarity for primary diagnosis confidence.
        secondary_min_threshold (float): Lower bound for secondary diagnosis candidate range.
        secondary_max_threshold (float): Upper bound for secondary diagnosis candidate range.
        llama (LlamaConfig): Translation model configuration.

    Returns:
        None: Dataclass instance used by app orchestration.

    Example:
        >>> config = AgentDiagnosisConfig.default()
    """

    root: Path
    output_dir: Path
    primary_threshold: float
    secondary_min_threshold: float
    secondary_max_threshold: float
    llama: LlamaConfig

    @property
    def output_full_dataset(self) -> Path:
        """Return target parquet path for full classified dataset.

        Args:
            None

        Returns:
            Path: Full output parquet path.

        Example:
            >>> config.output_full_dataset
        """
        return self.output_dir / "agent_outputs_dataset_sintomas_grupos_classificado.parquet"

    @property
    def output_unique_dataset(self) -> Path:
        """Return target parquet path for unique symptom combinations.

        Args:
            None

        Returns:
            Path: Unique output parquet path.

        Example:
            >>> config.output_unique_dataset
        """
        return self.output_dir / "agent_outputs_dataset_sintomas_agrupados_unicos_classificado.parquet"

    @classmethod
    def default(cls) -> "AgentDiagnosisConfig":
        """Build default production configuration from repository structure.

        Args:
            None

        Returns:
            AgentDiagnosisConfig: Path and threshold settings.

        Example:
            >>> AgentDiagnosisConfig.default()
        """
        root = find_project_root()
        output_dir = root / "src" / "outputs" / "genai"
        output_dir.mkdir(parents=True, exist_ok=True)
        return cls(
            root=root,
            output_dir=output_dir,
            primary_threshold=0.60,
            secondary_min_threshold=0.50,
            secondary_max_threshold=0.60,
            llama=LlamaConfig.default(),
        )

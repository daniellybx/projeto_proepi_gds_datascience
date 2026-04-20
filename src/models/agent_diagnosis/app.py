"""Run the production-grade diagnosis agent pipeline and export parquet outputs.

This application loads preprocessed data, performs symptom-based diagnosis
selection, translates diagnosis labels, and writes model-ready outputs.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.data.preprocessing import DiagnosisDataPreprocessor, PreprocessingPaths
from src.models.agent_diagnosis.config import AgentDiagnosisConfig
from src.models.agent_diagnosis.tools.data_selection import rank_all_diseases, rank_secondary_diseases
from src.models.agent_diagnosis.tools.translation import DiagnosisTranslator


class AgentDiagnosisApp:
    """Orchestrate full diagnosis generation flow from clustered symptom data.

    Args:
        config (AgentDiagnosisConfig): Runtime and output configuration.

    Returns:
        None: Application instance ready to run.

    Example:
        >>> app = AgentDiagnosisApp(AgentDiagnosisConfig.default())
    """

    def __init__(self, config: AgentDiagnosisConfig):
        self.config = config
        self.preprocessor = DiagnosisDataPreprocessor(PreprocessingPaths.default())
        self.translator = DiagnosisTranslator(
            ollama_host=config.llama.ollama_host,
            preferred_models=config.llama.preferred_models,
        )
        self.required_full_columns = ("report_created_at", "primary_diagnosis", "secondary_diagnoses")
        self.required_unique_columns = ("unique_id", "primary_diagnosis", "secondary_diagnoses")

    def classify_unique_symptom_sets(self, unique_df: pd.DataFrame, symptom_cols: list[str]) -> pd.DataFrame:
        """Generate primary and secondary diagnoses for unique symptom combinations.

        Args:
            unique_df (pd.DataFrame): Deduplicated symptom combinations.
            symptom_cols (list[str]): Symptom feature columns.

        Returns:
            pd.DataFrame: Classified unique combinations with diagnosis columns.

        Example:
            >>> classified = app.classify_unique_symptom_sets(unique_df, symptom_cols)
        """
        _, _, medley_symptom_cols, disease_frequency, disease_symptom_map = self.preprocessor.load_medley()
        output = unique_df.copy()
        for idx, row in output.iterrows():
            patient_symptoms = self.preprocessor.map_row_symptoms_to_english(row, symptom_cols, medley_symptom_cols)
            ranking = rank_all_diseases(patient_symptoms, disease_symptom_map, disease_frequency)
            if ranking:
                primary_en, primary_score = ranking[0]
            else:
                primary_en, primary_score = "Insufficient symptoms", 0.0
            if primary_score >= self.config.primary_threshold:
                secondary_en = rank_secondary_diseases(
                    patient_symptoms=patient_symptoms,
                    disease_symptom_map=disease_symptom_map,
                    disease_frequency=disease_frequency,
                    min_threshold=self.config.secondary_min_threshold,
                    max_threshold=self.config.secondary_max_threshold,
                )
            else:
                secondary_en = []
            output.at[idx, "primary_diagnosis"] = self.translator.translate_one(primary_en)
            output.at[idx, "secondary_diagnoses"] = "; ".join(self.translator.translate_many(secondary_en))
        return output

    def enforce_output_schema(
        self,
        classified_full_df: pd.DataFrame,
        classified_unique_df: pd.DataFrame,
        symptom_cols: list[str],
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Validate required columns and normalize output column order.

        Args:
            classified_full_df (pd.DataFrame): Full classified dataset.
            classified_unique_df (pd.DataFrame): Unique classified dataset.
            symptom_cols (list[str]): Symptom columns used in the merge.

        Returns:
            tuple[pd.DataFrame, pd.DataFrame]: Schema-validated full and unique outputs.

        Example:
            >>> full_df, unique_df = app.enforce_output_schema(full_df, unique_df, symptom_cols)
        """
        for column in self.required_full_columns:
            if column not in classified_full_df.columns:
                raise ValueError(f"Missing required full-output column: {column}")
        for column in self.required_unique_columns:
            if column not in classified_unique_df.columns:
                raise ValueError(f"Missing required unique-output column: {column}")
        fixed_unique_order = ["unique_id", *symptom_cols, "primary_diagnosis", "secondary_diagnoses"]
        classified_unique_df = classified_unique_df[[col for col in fixed_unique_order if col in classified_unique_df.columns]]
        full_cols = classified_full_df.columns.tolist()
        tail_cols = [col for col in ("primary_diagnosis", "secondary_diagnoses") if col in full_cols]
        body_cols = [col for col in full_cols if col not in tail_cols]
        classified_full_df = classified_full_df[body_cols + tail_cols]
        return classified_full_df, classified_unique_df

    def write_schema_contract(
        self,
        classified_full_df: pd.DataFrame,
        classified_unique_df: pd.DataFrame,
    ) -> Path:
        """Persist a JSON schema contract for downstream deploy integrations.

        Args:
            classified_full_df (pd.DataFrame): Full classified dataset.
            classified_unique_df (pd.DataFrame): Unique classified dataset.

        Returns:
            Path: Output schema contract JSON path.

        Example:
            >>> schema_path = app.write_schema_contract(full_df, unique_df)
        """
        schema_path = self.config.output_dir / "agent_diagnosis_output_schema.json"
        contract = {
            "full_output": {
                "path": str(self.config.output_full_dataset),
                "columns": classified_full_df.columns.tolist(),
                "required_columns": list(self.required_full_columns),
            },
            "unique_output": {
                "path": str(self.config.output_unique_dataset),
                "columns": classified_unique_df.columns.tolist(),
                "required_columns": list(self.required_unique_columns),
            },
        }
        schema_path.write_text(json.dumps(contract, ensure_ascii=False, indent=2), encoding="utf-8")
        return schema_path

    def run(self) -> tuple[Path, Path]:
        """Execute diagnosis pipeline and persist outputs as parquet datasets.

        Args:
            None

        Returns:
            tuple[Path, Path]: Full dataset and unique dataset output paths.

        Example:
            >>> app.run()
        """
        self.config.output_dir.mkdir(parents=True, exist_ok=True)
        proepi_df, symptom_cols = self.preprocessor.load_proepi_clusters()
        unique_df = self.preprocessor.build_unique_symptom_sets(proepi_df, symptom_cols)
        classified_unique_df = self.classify_unique_symptom_sets(unique_df, symptom_cols)
        classified_full_df = self.preprocessor.attach_classifications(proepi_df, classified_unique_df, symptom_cols)
        classified_full_df, classified_unique_df = self.enforce_output_schema(
            classified_full_df=classified_full_df,
            classified_unique_df=classified_unique_df,
            symptom_cols=symptom_cols,
        )
        classified_full_df.to_parquet(self.config.output_full_dataset, index=False)
        classified_unique_df.to_parquet(self.config.output_unique_dataset, index=False)
        self.write_schema_contract(classified_full_df, classified_unique_df)
        return self.config.output_full_dataset, self.config.output_unique_dataset


def main() -> None:
    """Run diagnosis app from command-line entry point.

    Args:
        None

    Returns:
        None: Writes parquet outputs to disk.

    Example:
        >>> main()
    """
    app = AgentDiagnosisApp(AgentDiagnosisConfig.default())
    full_path, unique_path = app.run()
    print(f"Generated full diagnosis parquet: {full_path}")
    print(f"Generated unique diagnosis parquet: {unique_path}")


if __name__ == "__main__":
    main()

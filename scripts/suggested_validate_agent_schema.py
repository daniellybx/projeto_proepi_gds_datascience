"""Suggested deploy-time validator for agent diagnosis output schema.

This script checks whether generated parquet outputs match the JSON schema
contract emitted by src/models/agent_diagnosis/app.py.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


def validate_schema(schema_path: Path) -> None:
    """Validate parquet outputs against the stored schema contract.

    Args:
        schema_path (Path): Path to agent_diagnosis_output_schema.json.

    Returns:
        None: Raises ValueError when schema is invalid.

    Example:
        >>> validate_schema(Path("src/outputs/genai/agent_diagnosis_output_schema.json"))
    """
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    for key in ("full_output", "unique_output"):
        output_meta = schema[key]
        parquet_path = Path(output_meta["path"])
        if not parquet_path.exists():
            raise ValueError(f"Missing parquet file: {parquet_path}")
        df = pd.read_parquet(parquet_path)
        missing_required = [col for col in output_meta["required_columns"] if col not in df.columns]
        if missing_required:
            raise ValueError(f"{key}: missing required columns: {missing_required}")
        declared_cols = output_meta["columns"]
        if df.columns.tolist() != declared_cols:
            raise ValueError(f"{key}: column order mismatch.")
    print("Schema validation succeeded for full_output and unique_output.")


def main() -> None:
    """Execute schema validation using default schema path.

    Args:
        None

    Returns:
        None: Prints validation status to stdout.

    Example:
        >>> main()
    """
    schema_path = Path("src/outputs/genai/agent_diagnosis_output_schema.json")
    validate_schema(schema_path)


if __name__ == "__main__":
    main()

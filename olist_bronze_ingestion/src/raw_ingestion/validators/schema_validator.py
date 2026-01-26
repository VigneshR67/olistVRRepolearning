#check if valid schema

from pyspark.sql import Dataframe
from pyspark.sql.types import StructType
from raw_ingestion.exceptions import SchemaValidationException

def _schema_to_dict(schema: StructType) -> dict:
    return {field.name: field.dataType.simpleSting() for field in schema.fields}

def validate_schema(df: Dataframe, expected_schema: StructType,strict: bool = True)-> None:
    """
    validates datafame schema against expected schema
    """

    if not isinstance(expected_schema, StructType):
        raise TypeError("expected_schema must be a pyspark.sql.types.StructType")

    actual_schema = _schema_to_dict(df.schema)
    expected_schema = _schema_to_dict(expected_schema)

      missing_cols = expected_cols - actual_cols
    if missing_cols:
        raise SchemaValidationException(
            f"Missing required columns: {sorted(missing_cols)}"
        )

    if strict:
        extra_cols = actual_cols - expected_cols
        if extra_cols:
            raise SchemaValidationException(
                f"Unexpected extra columns: {sorted(extra_cols)}"
            )

    mismatched_types = []
    for col in expected_cols & actual_cols:
        if actual[col] != expected[col]:
            mismatched_types.append(
                f"{col} (expected={expected[col]}, actual={actual[col]})"
            )

    if mismatched_types:
        raise SchemaValidationException(
            "Column type mismatch: " + ", ".join(mismatched_types)
        )
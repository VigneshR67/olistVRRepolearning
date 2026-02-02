#check if valid schema

from pyspark.sql import DataFrame
from pyspark.sql.types import StructType
from raw_ingestion.exceptions import SchemaValidationException

def _schema_to_dict(schema: StructType) -> dict:
    return {field.name: field.dataType.simpleString() for field in schema.fields}

def validate_schema(df: DataFrame, expected_schema: StructType,strict: bool = True)-> None:
    """
    validates datafame schema against expected schema
    """

    if not isinstance(expected_schema, StructType):
        raise TypeError("expected_schema must be a pyspark.sql.types.StructType")

    actual_schema = _schema_to_dict(df.schema)
    expected_schema = _schema_to_dict(expected_schema)

    actual_cols = set(actual_schema.keys())
    expected_cols = set(expected_schema.keys())
    
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
        if actual_schema[col] != expected_schema[col]:
            mismatched_types.append(
                f"{col} (expected={expected_schema[col]}, actual={actual_schema[col]})"
            )

    if mismatched_types:
        raise SchemaValidationException(
            "Column type mismatch: " + ", ".join(mismatched_types)
        )
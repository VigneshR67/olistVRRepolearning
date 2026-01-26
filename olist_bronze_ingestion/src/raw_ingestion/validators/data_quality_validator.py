from pyspark.sql import DataFrame
from pyspark.sql.functions import col
from raw_ingestion.exceptions import IngestionException


def validate_not_null(df: DataFrame, columns: list[str]) -> None:
    for column in columns:
        print(f"Count of nulls in column {column}: {df.filter(col(column).isNull()).count()}")
        if df.filter(col(column).isNull()).limit(1).count() > 0:
            raise IngestionException(
                f"Null values found in column: {column}"
            )

def validate_uniqueness(df: DataFrame, columns: list[str]) -> None:
    dup_count = (
        df.groupBy(columns)
        .count()
        .filter("count > 1")
        .limit(1)
        .count()
    )

    if dup_count > 0:
        raise IngestionException(
            f"Duplicate records found for columns: {columns}"
        )






import pytest
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from olist_bronze_ingestion.src.raw_ingestion.validators.data_quality_validator import *
from raw_ingestion.exceptions import IngestionException

def test_validate_not_null(spark):
    schema= StructType([
        StructField("id",StringType(),True),
        StructField("age",StringType(),True),
        StructField("date",StringType(),True)
    ])

    df = spark.createDataFrame([("1","22","01/30/2026"),("2",None,"01/30/2026"),("3",None,"01/30/2026")],schema=schema)

    try:
        validate_not_null(df,["age","date"])
    except Exception as e:
        print(e)
        assert e.__class__.__name__ == "IngestionException"
        assert "Null values found" in str(e)
    else:
        pytest.fail("No Exception raised")


def test_validate_uniqueness(spark):
    schema= StructType([
        StructField("id",StringType(),True),
        StructField("age",StringType(),True),
        StructField("date",StringType(),True)
    ])

    df = spark.createDataFrame([("1","22","01/30/2026"),("1",None,"01/30/2026"),("1",None,"01/30/2026")],schema=schema)

    try:
        validate_uniqueness(df,["id","date"])
    except Exception as e:
        print(e)
        assert e.__class__.__name__ == "IngestionException"
        assert "Duplicate records found" in str(e)
    else:
        pytest.fail("No Exception raised") 



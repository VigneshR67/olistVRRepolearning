import pytest
from pyspark.sql.types import StructType,StructField,StringType,IntegerType
from olist_bronze_ingestion.src.raw_ingestion.validators.schema_validator import _schema_to_dict,validate_schema
from olist_bronze_ingestion.src.raw_ingestion.exceptions import SchemaValidationException


def test_validate_schema_internal_schema_to_dict():
    schema = StructType([
        StructField("id",StringType(),True),
        StructField("age",IntegerType(),True)
    ])
    result = _schema_to_dict(schema)

    assert result =={"id":"string","age":"int"}

def test_validate_schema_internal_schema_to_dict_empty():
    schema = StructType([])

    assert _schema_to_dict(schema) =={}


def test_validate_schema_internal_schema_none_test():
    with pytest.raises(AttributeError):
        _schema_to_dict(None)

def test_validate_schema_success(spark):
    schema = StructType([
        StructField("name",StringType(),True),
        StructField("age",IntegerType(),True)
    ])

    df = spark.createDataFrame([("vr",20)],schema=schema)

    validate_schema(df,schema)

def test_validate_expected_schema_check(spark):
    schema = StructType([
        StructField("name",StringType(),True),
        StructField("age",IntegerType(),True)
    ])

    expected_schema = ([
        StructField("name",StringType(),True),
        StructField("age",IntegerType(),True)
    ])

    df = spark.createDataFrame([("vr",20)],schema=schema)

    with pytest.raises(TypeError) as exc:
        validate_schema(df,expected_schema)
    
    assert "expected_schema" in str(exc.value)

def test_validate_missing_col_check(spark):
    schema = StructType([
        StructField("name",StringType(),True)
    ])

    expected_schema = StructType([
        StructField("name",StringType(),True),
        StructField("age",IntegerType(),True)
    ])

    df = spark.createDataFrame([("vr",)],schema=schema)

    try:
        validate_schema(df,expected_schema)
    except Exception as e:
        print(type(e))
        print(e.__class__.__module__)
        assert e.__class__.__name__=="SchemaValidationException"
        assert "Missing required columns" in str(e)

def test_validate_actual_extra_col_check(spark):
    schema = StructType([
        StructField("id",IntegerType(),True),
        StructField("name",StringType(),True),
        StructField("date",StringType(),True)
    ])

    expected_schema = StructType([
        StructField("id",IntegerType(),True),
        StructField("name",StringType(),True)
    ])

    df = spark.createDataFrame([(1,"vr","1/2/2026")],schema=schema)
    try:
        validate_schema(df,expected_schema)
    except Exception as e:
        print(e)
        assert e.__class__.__name__ == "SchemaValidationException"
        assert "Unexpected extra" in str(e)

def test_validate_col_type_mismatch(spark):
    schema = StructType([
        StructField("id",IntegerType(),True),
        StructField("name",StringType(),True)
    ])

    expected_schema = StructType([
        StructField("id",IntegerType(),True),
        StructField("name",IntegerType(),True)
    ])

    df = spark.createDataFrame([(1,"vr",)],schema=schema)
    try:
        validate_schema(df,expected_schema)
    except Exception as e:
        print(e)
        assert e.__class__.__name__ == "SchemaValidationException"
        assert "Column type" in str(e)
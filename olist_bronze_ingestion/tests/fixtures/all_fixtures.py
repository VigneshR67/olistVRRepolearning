import pytest
from pathlib import Path
from pyspark.sql import SparkSession

@pytest.fixture
def sample_input():
    fixture_dir = Path(__file__).parent
    file_path=fixture_dir/"sample.csv"
    return file_path

@pytest.fixture(scope="session")
def spark():
    spark = (SparkSession.builder
             .master("local[1]")
             .appName("pytest-spark")
             .getOrCreate()
             )
    yield spark
    spark.stop()
fixture_dir = Path(__file__).parent
customer_source_path = fixture_dir/"customer_source.json"
@pytest.fixture
def customer_source():
    return customer_source_path
    

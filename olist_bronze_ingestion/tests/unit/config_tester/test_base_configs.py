import pytest
from olist_bronze_ingestion.src.raw_ingestion.configs.base_configs import load_source_config

def test_source_config_sucess(customer_source):

    result = load_source_config(customer_source)

    assert result.source_name =="olist_customers"
    assert result.file_format == "csv"


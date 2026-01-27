import pytest
from src.raw_ingestion.validators.ingestion_validations import validate_file_exists
from src.raw_ingestion.exceptions import FileRejectedException

def test_validate_file_exists_raises_exception():
    with pytest.raises(FileRejectedException):
        validate_file_exists("nonexistent_file.txt")
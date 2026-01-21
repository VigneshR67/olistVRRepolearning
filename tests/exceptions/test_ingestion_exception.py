import pytest

from src.raw_ingestion.exceptions import ( IngestionException,
    FileNotFoundException,
    SchemaValidationException,
    FileRejectedException)


def test_ingestion_exception():
    exc = IngestionException("generic failure")

    assert str(exc) == "generic failure"
    assert exc.reason == "generic failure"

def test_file_not_found_exception():
    with pytest.raises(FileNotFoundException) as exc:
        raise FileNotFoundException("file not found")

    assert isinstance(exc.value, IngestionException)
    assert exc.value.reason == "file not found"

def test_schema_validation_exception():
    with pytest.raises(SchemaValidationException) as exc:
        raise SchemaValidationException("schema validation failed")

    assert isinstance(exc.value, IngestionException)
    assert exc.value.reason == "schema validation failed"
    #assert exc.reason == "schema validation failed"

def test_file_rejected_exception():
    with pytest.raises(FileRejectedException) as exc:
        raise FileRejectedException(reason="file rejected",metadata={"check":"file rejection"})

    assert isinstance(exc.value, IngestionException)
    assert exc.value.reason == "file rejected"
    assert exc.value.metadata["check"]=="file rejection"

#further exceptions testing can be done on the validators

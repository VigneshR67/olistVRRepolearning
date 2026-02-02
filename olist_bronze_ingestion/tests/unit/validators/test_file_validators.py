import pytest
from olist_bronze_ingestion.src.raw_ingestion.validators.file_validators import *
from olist_bronze_ingestion.src.raw_ingestion.validators.schema_validator import *
from olist_bronze_ingestion.src.raw_ingestion.exceptions import FileNotFoundException,FileRejectedException

#pytest provides a tmp_path by default

def test_validate_file_exists(tmp_path):

    file_path = tmp_path/"test.txt"
    file_path.write_text("hello")

    validate_file_exists(file_path)

def test_validate_file_exists_exception(tmp_path):

    file_path = tmp_path/"missing.txt"

    try:
        validate_file_exists(str(file_path))
    except Exception as e:
        assert e.__class__.__name__ == "FileNotFoundException"
        assert "File was not in found" in str(e)
    else:
        pytest.fail("Exception was not raised")



def test_validate_file_not_empty(tmp_path):
    file_path=tmp_path/"missing.txt"
    file_path.write_text("")

    try:
        validate_file_not_empty(file_path)
    except Exception as e:
        assert e.__class__.__name__ == "FileRejectedException"
        assert "File is empty" in str(e)

def test_validate_file_not_empty_exception(tmp_path):
    file_path=tmp_path/"test2.txt"
    file_path.write_text("hello my world is important")


    validate_file_not_empty(file_path)


def test_validate_file_extension():
    sample_file = Path(__file__).parent/"unit/fixtures"/"sample.csv"

    validate_file_extension(sample_file,[".csv",".json"])

def test_validate_file_extension_exception(sample_input):
    sample_file = sample_input
    print(sample_file)
    
    try:
        validate_file_extension(sample_file,["csv",".json"])
    except Exception as e:
        print(e)
        assert e.__class__.__name__ =="FileRejectedException"
        assert "File extension is not valid" in str(e)
    else:
        pytest.fail("Exception was not raised")
        



    
    
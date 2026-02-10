from raw_ingestion.validators.file_validators import (validate_file_exists,
                                                      validate_file_not_empty,
                                                      validate_file_extension)

from raw_ingestion.validators.schema_validator import validate_schema
from raw_ingestion.validators.data_quality_validator import (validate_not_null,
                                                              validate_uniqueness)

File_validators={
    "file_exists":validate_file_exists,
    "file_not_empty":validate_file_not_empty,
    "file_extension":validate_file_extension
}

schema_validators = {
    "schema_validation":validate_schema
}

data_quality_validators ={
    "not_null":validate_not_null,
    "uniqueness":validate_uniqueness
}

def get_validators(validator_type:str,name:str):
    """
    create a registry for each validators
    dict: created with validator_type:nameofthevalidators pairs
    """
    registry = {
        "file":File_validators,
        "schema":schema_validators,
        "data_quality":data_quality_validators

    }

    try:
        return registry[validator_type][name]
    except KeyError:
        raise ValueError(f"Validator not found: type ={validator_type}, name ={name}")
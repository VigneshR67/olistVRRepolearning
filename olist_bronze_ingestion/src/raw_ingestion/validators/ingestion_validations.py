#All file rejection scenarios to be handled here
#1. schema mismatch
#2. file not found
#3. file is empty
#4. file is corrupt
#5. file is not in the expected format
#6. mandatory column for type2 tables.
#7. move the file to rejected folder.

from raw_ingestion.exceptions import FileRejectedException

def validate_file_exists(path:str):
    if not path:
        raise FileRejectedException(
            reason = "File path is empty",
            metadata={"check":"file_exists"}
            )
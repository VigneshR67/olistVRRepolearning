from pathlib import Path
import raw_ingestion.exceptions import FileNotFoundException,FileRejectedException

#pathlib is a python module alternative to os.path giving OOO approach to system path 
def validate_file_exists(file_path :str)-> None:
    """
        Validate that input file exists
    """
    if not Path(file_path).exists():
        raise FileNotFoundException(f"File was not in found in {file_path}")

def validate_file_not_empty(file_path :str)-> None:
    """
        Validate that input file is not empty
    """

    if Path(file_path).stat().st_size ==0:
        raise FileRejectedException(
            reason = f"File is empty",
            metadata = {"file_path":file_path})
        
def validate_file_extension(file_path :str,valid_extensions :list[str])-> None:
    """
        Validate that input file has valid extension
    """
    file_extension = Path(file_path).suffix
    if file_extension not in valid_extensions:
        raise FileRejectedException(
            reason = f"File extension is not valid",
            metadata = {"file_path":file_path,"valid_extensions":valid_extensions})
        
        
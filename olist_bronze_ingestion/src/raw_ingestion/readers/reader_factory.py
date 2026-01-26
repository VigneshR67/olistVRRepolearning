from raw_ingestion.readers.csv_reader import CsvReader
from raw_ingestion.readers.json_reader import JsonReader
from raw_ingestion.readers.parquet_reader import ParquetReader
from raw_ingestion.exceptions import IngestionException


def get_reader(file_format:str):
    readers ={
        "csv":CsvReader,
        "json":JsonReader,
        "parquet":ParquetReader
    }
    
    try:
        return readers[file_format.lower()]()
    except KeyError:
        raise IngestionException(f"Unsupported file format {file_format}")


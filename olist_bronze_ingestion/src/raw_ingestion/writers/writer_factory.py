from raw_ingestion.writers.base_writer import BaseWriter
from raw_ingestion.writers.delta_writer import DeltaWriter
from raw_ingestion.writers.table_writer import TableWriter
from raw_ingestion.exceptions import IngestionException

def get_writer(writer_format:str):
    writers ={
        "delta": DeltaWriter,
        "table": TableWriter
    }

    try:
        return writers[writer_format]()
    except KeyError:
        raise IngestionException(f"Invalid writer format: {writer_format}")
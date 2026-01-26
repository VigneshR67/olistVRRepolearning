
from raw_ingestion.writers.base_writer import BaseWriter
from raw_ingestion.exceptions import IngestionException

class TableWriter(BaseWriter):

    def write(self, df, target, write_mode, options=None):
        (
            df.write
              .mode(write_mode)
              .options(**(options or {}))
              .saveAsTable(target)
        )
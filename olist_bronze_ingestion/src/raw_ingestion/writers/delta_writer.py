from raw_ingestion.writers.base_writer import BaseWriter
from raw_ingestion.exceptions import IngestionException

class DeltaWriter(BaseWriter):

    #Default option can implemented here if required

    def write(self, df, target, write_mode, options=None):
        try:
            (
                df.write
                  .format("delta")
                  .mode(write_mode)
                  .options(**(options or {}))
                  .saveAsTable(target)
            )
        except Exception as e:
            raise IngestionException(
                f"Failed to write Delta table {target}"
            ) from e
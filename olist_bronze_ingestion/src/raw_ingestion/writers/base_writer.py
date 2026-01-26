from abc import ABC, abstractmethod
from pyspark.sql import DataFrame

class BaseWriter(ABC):

    @abstractmethod
    def write(
        self,
        df: DataFrame,
        target: str,
        write_mode: str,
        options: dict | None = None
    ):
        """
        df       : Spark DataFrame to write
        target   : table name or path
        write_mode: append / overwrite
        options  : Spark write options
        """
        pass
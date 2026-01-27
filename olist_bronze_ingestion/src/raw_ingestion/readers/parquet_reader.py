from .base_reader import BaseReader
from pyspark.sql import DataFrame

class ParquetReader(BaseReader):
   
    DEFAULT_OPTIONS = {
        "mergeSchema": "false"
    }

    def read(self,spark,path:str,read_options:dict|None=None, schema=None)->Dataframe:

    

    options = {
            **self.DEFAULT_OPTIONS,
            **(read_options or {})
        }
    
    reader = {
        spark.read.format("parquet").options(**options)
    }
    
    if schema:
        reader = reader.schema(schema)
    
    return reader.load(path)

from .base_reader import BaseReader
from pyspark.sql import DataFrame

class CsvReader(BaseReader):

    DEFAULT_OPTIONS = {
        "header": "true",
        "inferSchema": "false",
        "mode": "FAILFAST"
    }
    
    def read(self,spark,path:str,read_options:dict|None=None, schema=None)->DataFrame:

    

        options = {
            **self.DEFAULT_OPTIONS,
            **(read_options or {})
        }
    
        reader = spark.read.format("csv").options(**options)
        
    
        if schema:
             reader = reader.schema(schema)
        df = reader.load(path)

        return df

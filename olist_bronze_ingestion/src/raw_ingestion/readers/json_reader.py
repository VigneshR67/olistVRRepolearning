from .base_reader import BaseReader
from pyspark.sql import DataFrame

class JsonReader(BaseReader):

    DEFAULT_OPTIONS = {
        "multiLine": "false",
        "mode": "FAILFAST"
    }
    
    def read(self,spark,path:str,read_options:dict|None=None, schema=None)->DataFrame:

    

        options = {
            **self.DEFAULT_OPTIONS,
            **(read_options or {})
         }
    
        reader = {
             spark.read.format("json").options(**options)
            }
    
        if schema:
             reader = reader.schema(schema)
    
        return reader.load(path)

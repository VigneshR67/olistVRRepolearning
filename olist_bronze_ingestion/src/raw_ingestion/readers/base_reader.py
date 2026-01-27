from abc import ABC, abstractmethod
from pyspark.sql import DataFrame

class BaseReader(ABC):
    @abstractmethod
    def read(self,spark,path:str,read_options:dict|None=None,schema=None)->Dataframe:
        pass


# class BaseReader(ABC):

#     def read(self, spark, path: str):
#         self._pre_read()
#         df = self._do_read(spark, path)
#         self._post_read(df)
#         return df

#     def _pre_read(self):
#         print("Common pre-read logic")

#     @abstractmethod
#     def _do_read(self, spark, path: str):
#         pass

#     def _post_read(self, df):
#         print("Common post-read logic")

# class CustomCsvReader(BaseReader):

#     def _do_read(self, spark, path: str):
#         df = super()._do_read(spark, path)  # if defined
#         return df.filter("status = 'ACTIVE'")


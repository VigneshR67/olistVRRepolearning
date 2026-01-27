#only exceptions to be implemented here. will need more insights on this one to implement the exceptions ( I guess this will be the error message we want to present the user)

class IngestionException(Exception):
    """Base class for all ingestion-related exceptions"""

    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason

class FileNotFoundException(IngestionException):
    pass

class SchemaValidationException(IngestionException):
    pass


class FileRejectedException(IngestionException):
    #controlled rejected - should not fail pipeline
    def __init__(self,reason: str, metadata : dict| None = None):
        super().__init__(reason) # call the main Exception class and passes reason as the parameter to raise an exception
        self.metadata = metadata or {}
        
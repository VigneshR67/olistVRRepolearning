from raw_ingestion.audit import audit_step
from raw_ingestion.logging_utils import log_execution, retry

def execute_read(context, reader, schema):
    @log_execution("READ")
    @audit_step("read", context.audit_collector)
    @retry(retries=3, delay_seconds=5)
    def _read():
        return reader.read(
            spark=context.spark,
            path=context.config.source_path,
            read_options=context.config.read_options,
            schema=schema
        )

    return _read()

def execute_validation(context, df, validators):
    @log_execution("VALIDATION")
    @audit_step("validate", context.audit_collector)
    def _validate():
        for validator in validators:
            validator(df)
        return df

    return _validate()

def execute_write(context, writer, df):
    @log_execution("WRITE")
    @audit_step("write", context.audit_collector)
    @retry(retries=2, delay_seconds=3)
    def _write():
        return writer.write(df)

    return _write()

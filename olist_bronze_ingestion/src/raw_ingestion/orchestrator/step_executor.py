from raw_ingestion.audit import audit_step
from raw_ingestion.common_logging import log_execution, retry
from pyspark.sql import DataFrame


def execute_read(context, reader, schema):
    @log_execution("READ")
    @audit_step("read", context.audit_collector)
    @retry(retries=3, delay_seconds=5)
    def _read()->DataFrame:
        read_options = (
            context.config.read_options.to_dict()
            if context.config.read_options
            else None
        )

        context.logger.info(
            f"read_options type after conversion: {type(read_options)}"
        )
        df = reader.read(
            spark=context.spark,
            path=context.source_path,
            read_options=read_options,
            schema=schema
        )
        return df

    return _read()

def execute_validation(context, df, validators,schema):
    @log_execution("VALIDATION")
    @audit_step("validate", context.audit_collector)
    def _validate():
        for validator in validators:
            validator(df,schema)
        return df

    return _validate()

def execute_write(context, writer, df, target):
    @log_execution("WRITE")
    @audit_step("write", context.audit_collector)
    @retry(retries=2, delay_seconds=3)
    def _write():
        return writer.write(df,target,"append")

    return _write()

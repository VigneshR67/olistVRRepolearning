from raw_ingestion.orchestrator.pipeline_context import PipelineContext
from raw_ingestion.orchestrator.step_executor import (
    execute_read,
    execute_validation,
    execute_write
)
from raw_ingestion.readers import reader_factory
from raw_ingestion.writers import writer_factory
from raw_ingestion.validators.validator_registry import get_validators
from raw_ingestion.ingestion.schema_loader import load_schema
from raw_ingestion.audit import AuditWriter


def run_pipeline(spark, config,input_path):
    """
    Main entry point for raw ingestion pipeline.
    """

    context = PipelineContext(spark, config,input_path)

    try:
        context.logger.info("Pipeline started")

        # 1️⃣ Load schema
        schema = load_schema(
            spark=spark,
            schemaPath=config.schema.schema_file,
            enforce_strict=False,
            context=context
        )

        # 2️⃣ Reader
        reader = reader_factory.get_reader(config.file_format)
        
        context.logger.info(f"Output of schema:{schema}")
        # 3️⃣ Read
        df = execute_read(context, reader, schema)
        df.show(10)
        # 4️⃣ Validators
        # validators = [
        #     get_validators("schema", "schema"),
        #     *[
        #         get_validators("data_quality", rule)
        #         for rule in config.data_quality_rules
        #     ]
        # ]

        validators = [
            get_validators("schema", "schema_validation")
        ]
        context.logger.info(f"Output of validators:{validators}")

        df = execute_validation(context, df, validators,schema)

        # # 5️⃣ Writer
        writer = writer_factory.get_writer(config.writer_format)

        df = execute_write(context, writer, df,config.raw_table)

        context.logger.info("Pipeline completed successfully")

    finally:
        # 6️⃣ Persist audit (always)
        #print("Audit")
        #print(context.audit_collector.all())
        AuditWriter().write(
            context.audit_collector.all(),
            output_path=f"{config.audit_path}/audit.json"
        )

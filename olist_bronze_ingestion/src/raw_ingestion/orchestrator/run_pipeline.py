from raw_ingestion.orchestrator.pipeline_context import PipelineContext
from raw_ingestion.orchestrator.step_executor import (
    execute_read,
    execute_validation,
    execute_write
)

from raw_ingestion.readers import ReaderFactory
from raw_ingestion.writers import WriterFactory
from raw_ingestion.validators import get_validator
from raw_ingestion.schema.schema_loader import load_schema
from raw_ingestion.audit import AuditWriter


def run_pipeline(spark, config):
    """
    Main entry point for raw ingestion pipeline.
    """

    context = PipelineContext(spark, config)

    try:
        context.logger.info("Pipeline started")

        # 1️⃣ Load schema
        schema = load_schema(
            spark=spark,
            schema_file=config.schema.schema_file
        )

        # 2️⃣ Reader
        reader = ReaderFactory.get(config.format)

        # 3️⃣ Read
        df = execute_read(context, reader, schema)

        # 4️⃣ Validators
        validators = [
            get_validator("schema", "schema"),
            *[
                get_validator("data_quality", rule)
                for rule in config.data_quality_rules
            ]
        ]

        df = execute_validation(context, df, validators)

        # 5️⃣ Writer
        writer = WriterFactory.get(config.target)

        execute_write(context, writer, df)

        context.logger.info("Pipeline completed successfully")

    finally:
        # 6️⃣ Persist audit (always)
        AuditWriter().write(
            context.audit_collector.all(),
            output_path=f"{config.audit_path}/audit.json"
        )

from raw_ingestion.audit import AuditCollector
from raw_ingestion.common_logging import get_logger


class PipelineContext:
    """
    Holds shared objects for a pipeline run.
    """

    def __init__(self, spark, config,input_path):
        self.spark = spark
        self.config = config
        self.source_path = input_path
        self.audit_collector = AuditCollector()
        self.logger = get_logger("raw_ingestion.orchestrator")

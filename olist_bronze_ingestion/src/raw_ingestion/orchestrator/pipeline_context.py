from raw_ingestion.audit import AuditCollector
from raw_ingestion.logging_utils import get_logger


class PipelineContext:
    """
    Holds shared objects for a pipeline run.
    """

    def __init__(self, spark, config):
        self.spark = spark
        self.config = config
        self.audit_collector = AuditCollector()
        self.logger = get_logger("raw_ingestion.orchestrator")

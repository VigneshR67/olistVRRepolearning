from typing import List
from raw_ingestion.audit.audit_model import AuditRecord


class AuditCollector:
    """
    Holds audit records during pipeline execution.
    """

    def __init__(self):
        self._records: List[AuditRecord] = []

    def add(self, record: AuditRecord) -> None:
        self._records.append(record)

    def all(self) -> List[AuditRecord]:
        return self._records

import json
from pathlib import Path
from typing import List
from raw_ingestion.audit.audit_model import AuditRecord


class AuditWriter:
    """
    Writes audit records to JSON file.
    """

    def write(
        self,
        records: List[AuditRecord],
        output_path: str
    ) -> None:

        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        payload = [record.to_dict() for record in records]

        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)

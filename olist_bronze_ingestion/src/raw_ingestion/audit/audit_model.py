from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass
class AuditRecord:
    pipeline_name: str
    step_name: str
    status: str  # SUCCESS | FAILED | REJECTED
    start_time: str
    end_time: str
    duration_seconds: float

    records_read: Optional[int] = None
    records_written: Optional[int] = None

    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> dict:
        return asdict(self)


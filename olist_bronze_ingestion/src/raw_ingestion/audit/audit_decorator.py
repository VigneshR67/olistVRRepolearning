import time
from datetime import datetime
from functools import wraps
from raw_ingestion.audit.audit_model import AuditRecord


def audit_step(step_name: str, collector):
    """
    Audits execution of a pipeline step.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_ts = time.time()
            start_time = datetime.utcnow().isoformat()

            try:
                result = func(*args, **kwargs)

                end_ts = time.time()
                collector.add(
                    AuditRecord(
                        pipeline_name="raw_ingestion",
                        step_name=step_name,
                        status="SUCCESS",
                        start_time=start_time,
                        end_time=datetime.utcnow().isoformat(),
                        duration_seconds=round(end_ts - start_ts, 3),
                        records_read=result.count() if hasattr(result, "count") else None
                        if step_name == "read" else None,
                        records_written=result.count() if hasattr(result, "count") else None
                        if step_name == "write" else None
                    )
                )

                return result

            except Exception as e:
                end_ts = time.time()
                collector.add(
                    AuditRecord(
                        pipeline_name="raw_ingestion",
                        step_name=step_name,
                        status="FAILED",
                        start_time=start_time,
                        end_time=datetime.utcnow().isoformat(),
                        duration_seconds=round(end_ts - start_ts, 3),
                        error_message=str(e)
                    )
                )
                raise

        return wrapper

    return decorator

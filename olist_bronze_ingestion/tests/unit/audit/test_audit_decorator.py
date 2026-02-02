class FakeCollector:
    def __init__(self):
        self.records = []

    def add(self,record):
        self.records.append(record)


import pytest
from olist_bronze_ingestion.src.raw_ingestion.audit.audit_decorator import audit_step
from olist_bronze_ingestion.src.raw_ingestion.audit.audit_model import AuditRecord
from olist_bronze_ingestion.src.raw_ingestion.audit.audit_collector import AuditCollector

def test_audit_read_sucess():

    collector = FakeCollector()

    class Result:
        count =10

    
    @audit_step(step_name="read",collector=collector)
    def wrapper():
        return Result()

    result = wrapper()

    assert isinstance(result,Result)

    assert len(collector.records)==1
    record = collector.records[0]

    assert record.pipeline_name =="raw_ingestion"
    assert record.status =="SUCCESS"
    assert record.records_read == 10
    assert record.duration_seconds >=0

def test_audit_record_written():

    collector = AuditCollector()

    class Result:
        count = 5

    @audit_step(step_name="write",collector=collector)
    def wrapper():
        return Result()

    result = wrapper()

    assert isinstance(result,Result)

    assert len(collector._records)==1
    record = collector._records[0]
    print("testing record result",record.records_written)
    assert record.pipeline_name =="raw_ingestion"
    assert record.status=="SUCCESS"
    assert record.records_written == 5


def test_audit_step_failure():

    collector = AuditCollector()

    @audit_step(step_name="read",collector=collector)
    def wrapper():
        raise ValueError("boom")

    with pytest.raises(ValueError):
        wrapper()

    assert len(collector._records)==1
    record = collector._records[0]

    print("testing record",record.status)
    assert record.status =="FAILED"
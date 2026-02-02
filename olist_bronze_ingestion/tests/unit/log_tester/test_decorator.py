import pytest
import logging
from olist_bronze_ingestion.src.raw_ingestion.common_logging import *

def test_log_execution_sucess(caplog):

    @log_execution(step_name="dummy")
    def dummy():
        return 42

    with caplog.at_level(logging.INFO):
        result=dummy()

    assert result == 42
    assert "[START] dummy" in caplog.text
    assert "[END] dummy" in caplog.text

class log_retries:
    def __init__(self,fail_times):
        self.call =0
        self.fail_times= fail_times

    def __call__(self):
        self.call+=1
        if self.call <=self.fail_times:
            raise ValueError("temporary failure")
        return "success"



def test_log_exection_retries_happy(monkeypatch):
    monkeypatch.setattr("time.sleep",lambda _:None)

    logretries = log_retries(fail_times=2)

    @retry(retries = 3)
    def wrapped():
        return logretries()

    result = wrapped()

    assert result =="success"
    assert logretries.call ==3

def test_log_exection_retries_failure(monkeypatch):
    monkeypatch.setattr("time.sleep",lambda _:None)

    logretries = log_retries(fail_times=5)

    @retry(retries = 3)
    def wrapped():
        return logretries()

    with pytest.raises(ValueError):
        wrapped()

    assert logretries.call ==3

def test_log_execution_specific_error(monkeypatch):
    monkeypatch.setattr("time.sleep",lambda _:None)

    class CustomError(Exception):
        pass

    calls = {"count":0}

    @retry(retries=3,retry_on=(CustomError,))
    def wrapped():
        calls["count"]+=1
        raise ValueError("my error check")

    with pytest.raises(ValueError):
        wrapped()

    assert calls["count"]==1


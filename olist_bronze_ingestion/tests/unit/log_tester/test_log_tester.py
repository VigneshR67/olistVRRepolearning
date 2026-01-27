from src.raw_ingestion.common_logging import get_logger
import logging

def test_log_get_name():
    logger = get_logger("test ingestion")

    assert logger.name == "test ingestion"
    assert logger.level == logging.INFO


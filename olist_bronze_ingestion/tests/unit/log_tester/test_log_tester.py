from olist_bronze_ingestion.src.raw_ingestion.common_logging import get_logger
import logging

def test_log_get_name():
    logger = get_logger("test ingestion")
    print(logger.name)
    print(logger.level)

    assert logger.name == "test ingestion"
    assert logger.level == logging.INFO

def test_log_handlers_duplicate():
    logger1= get_logger("dup_test")
    print(logger1)
    handler_count = len(logger1.handlers)

    logger2 = get_logger("dup_test")
    print(logger2)

    assert logger1 == logger2

def test_logger_emits_logs(caplog):
    logger = get_logger("emit_test")

    with caplog.at_level(logging.INFO):
        logger.info("vignesh is here in this world")

    assert "vignesh is here in this world" in caplog.text
    assert "emit_test" in caplog.text




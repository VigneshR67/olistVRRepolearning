import time
import functools
from typing import Callable, Type
from raw_ingestion.common_logging.logger import get_logger


def log_execution(step_name: str | None = None):
    """
    Logs start, end, and execution time of a function.
    """

    def decorator(func: Callable):
        logger = get_logger(func.__module__)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            name = step_name or func.__name__
            start = time.time()

            logger.info(f"[START] {name}")

            try:
                result = func(*args, **kwargs)
                duration = round(time.time() - start, 3)

                logger.info(f"[END] {name} | duration={duration}s")
                return result

            except Exception as e:
                duration = round(time.time() - start, 3)
                logger.error(
                    f"[FAIL] {name} | duration={duration}s | error={e}",
                    exc_info=True
                )
                raise

        return wrapper

    return decorator



def retry(
    retries: int = 3,
    delay_seconds: int = 2,
    retry_on: tuple[Type[Exception], ...] = (Exception,)
):
    """
    Retries function execution on failure.
    """

    def decorator(func: Callable):
        logger = get_logger(func.__module__)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 1

            while True:
                try:
                    return func(*args, **kwargs)

                except retry_on as e:
                    if attempt >= retries:
                        logger.error(
                            f"[RETRY-FAILED] {func.__name__} | attempts={attempt}"
                        )
                        raise

                    logger.warning(
                        f"[RETRY] {func.__name__} | attempt={attempt}/{retries} | error={e}"
                    )

                    time.sleep(delay_seconds)
                    attempt += 1

        return wrapper

    return decorator

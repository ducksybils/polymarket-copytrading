from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
from functools import wraps
from .config import CONFIG


def clob_retry(func):
    """Decorator for retrying CLOB operations"""
    @wraps(func)
    @retry(
        stop=stop_after_attempt(CONFIG.retry_attempts),
        wait=wait_fixed(CONFIG.retry_delay),
        retry=retry_if_exception_type((Exception, ConnectionError, TimeoutError)),
        reraise=True
    )
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

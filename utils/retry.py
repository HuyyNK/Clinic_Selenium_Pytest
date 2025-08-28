"""Retry utility for test automation."""

import time
import logging
import config.config as cfg

logger = logging.getLogger(__name__)

def retry_on_failure(max_attempts=cfg.MAX_RETRY_ATTEMPTS):
    """Decorator to retry a function if it fails."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.warning(f"[Retry {attempt + 1}/{max_attempts}] {func.__name__} failed: {e}")
                    if attempt == max_attempts - 1:
                        if args and hasattr(args[0], "driver"):
                            args[0].driver.save_screenshot(f"error_{func.__name__}_attempt{attempt}.png")
                        raise
                    time.sleep(2)
        return wrapper
    return decorator
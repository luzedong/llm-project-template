"""重试装饰器"""
import time
from functools import wraps
from typing import Callable

from loguru import logger

import config


def retry_on_failure(
    max_retries: int = None,
    initial_delay: float = None,
    max_delay: float = None
):
    """重试装饰器

    Args:
        max_retries: 最大重试次数
        initial_delay: 初始延迟时间（秒）
        max_delay: 最大延迟时间（秒）
    """
    max_retries = max_retries or config.MAX_RETRIES
    initial_delay = initial_delay or config.RETRY_DELAY
    max_delay = max_delay or config.MAX_RETRY_DELAY

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay

            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        logger.error(f"执行失败，已重试{max_retries}次: {e}")
                        raise

                    logger.warning(f"执行失败 (尝试 {attempt + 1}/{max_retries}): {e}")
                    logger.info(f"等待 {delay:.1f} 秒后重试...")
                    time.sleep(delay)
                    delay = min(delay * 2, max_delay)

            raise RuntimeError("不应到达此处")

        return wrapper

    return decorator

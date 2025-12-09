"""日志工具"""
import sys
from pathlib import Path

from loguru import logger

import config


def setup_logger(log_file: str = "app.log"):
    """设置日志系统

    Args:
        log_file: 日志文件名
    """
    # 移除默认handler
    logger.remove()

    # 控制台输出
    logger.add(
        sys.stderr,
        format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
        level=config.LOG_LEVEL,
        colorize=True
    )

    # 文件输出
    log_dir = Path(config.LOG_DIR)
    log_dir.mkdir(parents=True, exist_ok=True)

    logger.add(
        log_dir / log_file,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
        level=config.LOG_LEVEL,
        rotation="100 MB",
        retention="7 days",
        encoding="utf-8"
    )

    return logger

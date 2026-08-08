import sys

from loguru import logger

logger.remove()

logger.add(
    sys.stdout,
    level="INFO",
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | {message}"
    ),
)

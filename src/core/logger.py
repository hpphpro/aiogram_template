import logging

from src.core.settings import (
    DATETIME_FORMAT,
    LOGGING_FORMAT,
    PROJECT_NAME,
)
from src.core.settings import LOG_LEVEL as LOG_LEVEL

logging.basicConfig(level=LOG_LEVEL, format=LOGGING_FORMAT, datefmt=DATETIME_FORMAT)

log = logging.getLogger(PROJECT_NAME)

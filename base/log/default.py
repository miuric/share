import logging
import sys

from loguru import logger

from config import STDERR_DEBUG_LEVEL

config = {
    "handlers": [
        {"sink": sys.stderr, "level": STDERR_DEBUG_LEVEL, 'backtrace': False, 'diagnose': False},
    ],
    "extra": {
        "user": "someone",
    }
}

logger.configure(**config)


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

# logging.basicConfig(handlers=[InterceptHandler()], level=0)

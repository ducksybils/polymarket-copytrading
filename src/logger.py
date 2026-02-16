import logging
import sys
from .config import CONFIG

# Flag to prevent multiple basicConfig calls
_logger_initialized = False


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for console output"""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{log_color}{record.levelname}{self.RESET}"
        return super().format(record)


def setup():
    """Setup logging configuration (only once)"""
    global _logger_initialized
    
    if _logger_initialized:
        return logging.getLogger("PolyCopy")
    
    level = getattr(logging, CONFIG.log_level.upper(), logging.INFO)
    
    handler = logging.StreamHandler(sys.stdout)
    formatter = ColoredFormatter(
        "%(asctime)s | %(levelname)-7s | %(name)-20s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    
    logger = logging.getLogger("PolyCopy")
    logger.setLevel(level)
    logger.addHandler(handler)
    
    _logger_initialized = True
    return logger

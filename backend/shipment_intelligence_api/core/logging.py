import logging
import logging.handlers
from pathlib import Path
from shipment_intelligence_api.core.settings import settings
from shipment_intelligence_api.core.constants import Environment

LOGGER_NAME = "shipment-intelligence-api"
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"


def _configure_logging() -> logging.Logger:
    """Configure logging for the application."""
    LOG_DIR.mkdir(exist_ok=True)

    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    )

    level = (
        logging.DEBUG
        if settings.ENVIRONMENT == Environment.DEVELOPMENT
        else logging.INFO
    )

    # Console handlers
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    # File handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_DIR / "app.log", maxBytes=10485760, backupCount=5
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


def get_logger(name: str | None = None) -> logging.Logger:
    """Get a logger instance."""
    _configure_logging()
    if name:
        return logging.getLogger(f"{LOGGER_NAME}.{name}")
    return logging.getLogger(LOGGER_NAME)

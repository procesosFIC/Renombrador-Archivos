import logging
from pathlib import Path

_LOGGER_NAME = "RenamerApp"
_LOG_FILE = Path("logs/renombramiento.log")


def get_app_logger() -> logging.Logger:
    """Return a singleton logger configured to persist errors in logs/renombramiento.log."""
    logger = logging.getLogger(_LOGGER_NAME)
    if logger.handlers:
        return logger

    logger.setLevel(logging.ERROR)
    _LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    file_handler = logging.FileHandler(_LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.ERROR)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.propagate = False

    return logger
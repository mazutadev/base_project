"""
Logger module.
"""

# Imports from standard library
import os
from typing import Optional

# Imports from third party libraries
import logging
from logging.handlers import RotatingFileHandler

# Imports from local modules
from .value_objects import LogConfig


# Try set colormode output
try:
    import colorlog

    COLORLOG_INSTALLED = True
except ImportError:
    COLORLOG_INSTALLED = False


def get_logger(config: Optional[LogConfig] = None, **kwargs) -> logging.Logger:
    """
    Get instance of logger.
    """

    # Allow legacy kwargs for backward compatibility
    for key in [
        "name",
        "level",
        "handlers",
        "file_config",
        "fmt",
        "datefmt",
        "propagate",
        "use_colors",
    ]:
        if key in kwargs and getattr(config, key, None) is None:
            setattr(config, key, kwargs[key])

    # Create logger
    logger = logging.getLogger(config.name)

    # Configure logger
    logger.setLevel(config.level)
    logger.propagate = config.propagate

    log_format = config.fmt or (
        "[%(asctime)s] %(levelname)s " "[%(name)s:%(lineno)d] %(message)s"
    )

    log_datefmt = config.datefmt or "%Y-%m-%d %H:%M:%S"

    # Configure console handler
    if "console" in config.handlers:

        # Configure colorized output if supported
        if config.use_colors and COLORLOG_INSTALLED:
            color_formatter = colorlog.ColoredFormatter(
                "%(log_color)s" + log_format,
                datefmt=log_datefmt,
                log_colors={
                    "DEBUG": "cyan",
                    "INFO": "green",
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "bold_red",
                },
            )
            ch = logging.StreamHandler()
            ch.setFormatter(color_formatter)

        # Configure plain text output if not supported
        else:
            formatter = logging.Formatter(log_format, datefmt=log_datefmt)
            ch = logging.StreamHandler()
            ch.setFormatter(formatter)

        # Add handler to logger

        if not any(
            isinstance(handler, logging.StreamHandler) for handler in logger.handlers
        ):
            logger.addHandler(ch)

    # Configure file handler
    if "file" in config.handlers and config.file_config:

        # Get path and name from config
        path = config.file_config.get("path", "logs")
        name = config.file_config.get("name", "app.log")

        # Create log directory if it doesn't exist
        os.makedirs(path, exist_ok=True)

        # Get file path, max bytes, and backup count from config
        file_path = os.path.join(path, name)
        max_bytes = config.file_config.get("max_bytes", 10 * 1024 * 1024)
        backup_count = config.file_config.get("backup_count", 5)

        fh = None

        # Create rotating file handler if max bytes is set
        if max_bytes > 0:
            fh = RotatingFileHandler(
                file_path,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding="utf-8",
            )

        # Create file handler if max bytes is not set
        else:
            if not any(
                isinstance(handler, logging.FileHandler) for handler in logger.handlers
            ):
                fh = logging.FileHandler(file_path, encoding="utf-8")

        if fh is not None:
            # Configure formatter
            formatter = logging.Formatter(log_format, datefmt=log_datefmt)
            fh.setFormatter(logging.Formatter(log_format, datefmt=log_datefmt))

            # Add handler to logger
            logger.addHandler(fh)

    return logger

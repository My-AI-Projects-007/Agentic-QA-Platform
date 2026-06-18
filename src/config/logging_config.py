"""Logging configuration"""
import logging
import logging.handlers
import os
from pathlib import Path
from src.config.settings import settings

# Create logs directory if it doesn't exist
log_dir = Path(settings.LOG_FILE).parent
log_dir.mkdir(parents=True, exist_ok=True)

# Configure logging
logger = logging.getLogger("agentic_qa_platform")
logger.setLevel(getattr(logging, settings.LOG_LEVEL))

# File handler
file_handler = logging.handlers.RotatingFileHandler(
    settings.LOG_FILE,
    maxBytes=10485760,  # 10MB
    backupCount=5
)
file_handler.setLevel(getattr(logging, settings.LOG_LEVEL))

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(getattr(logging, settings.LOG_LEVEL))

# Formatter
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance"""
    return logging.getLogger(f"agentic_qa_platform.{name}")

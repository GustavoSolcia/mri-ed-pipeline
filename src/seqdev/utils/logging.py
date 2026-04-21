"""Config to standardize and centralize logging."""

import logging

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    datefmt='%Y-%m-%d %H:%M:%S'
)

# NOTE: We are defining a single logger for everything
logger = logging.getLogger()

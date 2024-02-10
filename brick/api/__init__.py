import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,  # (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="/tmp/brick.log" if Path("/tmp").exists() else None,
    filemode="w",
)

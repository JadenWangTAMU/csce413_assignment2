"""Logging helpers for the honeypot."""

import logging
import os

LOG_PATH = "/app/logs/honeypot.log"


def create_logger():
    os.makedirs("/app/logs", exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(LOG_PATH), logging.StreamHandler()],
    )

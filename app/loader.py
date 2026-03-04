"""
Load generator: periodically triggers service A to produce distributed traces.
"""
import logging
import os
import time
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SERVICE_A_URL = os.environ.get("SERVICE_A_URL", "http://127.0.0.1:8000")
INTERVAL_SECONDS = float(os.environ.get("TELEMETRY_INTERVAL_SECONDS", "5"))


def main():
    logger.info(
        "Loader started: hitting %s every %s seconds",
        SERVICE_A_URL,
        INTERVAL_SECONDS,
    )
    while True:
        try:
            r = requests.get(f"{SERVICE_A_URL}/request", timeout=15)
            logger.debug("Trigger response: %s %s", r.status_code, r.text[:80])
        except Exception as e:
            logger.warning("Trigger failed: %s", e)
        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    main()

"""
Backend service (C). Does work and occasionally fails for realistic trace testing.
"""
import logging
import os
import random
from flask import Flask, jsonify

logger = logging.getLogger(__name__)
app = Flask(__name__)

FAILURE_RATE = float(os.environ.get("FAILURE_RATE", "0.1"))


@app.route("/work")
def work():
    if random.random() < FAILURE_RATE:
        logger.warning("Simulated failure in service-c", extra={"failure": True})
        return jsonify({"error": "simulated failure"}), 500
    logger.info("Work completed", extra={"service": "c"})
    return jsonify({"status": "ok", "service": "c"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8002"))
    app.run(host="127.0.0.1", port=port)

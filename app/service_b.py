"""
Middleware service (B). Calls service C.
"""
import logging
import os
import requests
from flask import Flask, jsonify

logger = logging.getLogger(__name__)
app = Flask(__name__)

SERVICE_C_URL = os.environ.get("SERVICE_C_URL", "http://127.0.0.1:8002")


@app.route("/process")
def process():
    try:
        r = requests.get(f"{SERVICE_C_URL}/work", timeout=5)
        r.raise_for_status()
        data = r.json()
        logger.info("Processed via service-c", extra={"status": data.get("status")})
        return jsonify({"status": "ok", "service": "b", "backend": data})
    except Exception as e:
        logger.exception("Call to service-c failed")
        return jsonify({"error": str(e)}), 502


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8001"))
    app.run(host="127.0.0.1", port=port)

"""
Frontend service (A). Entry point; calls service B.
"""
import logging
import os
import requests
from flask import Flask, jsonify

logger = logging.getLogger(__name__)
app = Flask(__name__)

SERVICE_B_URL = os.environ.get("SERVICE_B_URL", "http://127.0.0.1:8001")


@app.route("/")
@app.route("/request")
def request_handler():
    try:
        r = requests.get(f"{SERVICE_B_URL}/process", timeout=10)
        data = r.json() if r.ok else {"error": r.text}
        logger.info("Request completed", extra={"status_code": r.status_code})
        return jsonify({"status": "ok", "service": "a", "response": data}), r.status_code
    except Exception as e:
        logger.exception("Call to service-b failed")
        return jsonify({"error": str(e)}), 502


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    app.run(host="127.0.0.1", port=port)

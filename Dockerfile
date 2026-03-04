# Small image for OpenTelemetry pipeline testing: one container, three logical services.
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
# Install dependencies and auto-instrumentations (Flask, requests, logging)
RUN pip install --no-cache-dir -r requirements.txt && \
    opentelemetry-bootstrap -a install

COPY app/ ./app/
COPY run.sh ./
RUN chmod +x run.sh

# All configuration via environment variables (see README).
# Required: OTEL_EXPORTER_OTLP_ENDPOINT (e.g. http://collector:4318)
# Optional: TELEMETRY_INTERVAL_SECONDS, FAILURE_RATE, OTEL_SERVICE_NAME, etc.
ENTRYPOINT ["./run.sh"]

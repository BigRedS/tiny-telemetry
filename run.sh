#!/bin/sh
set -e

# Enable OTel logging: capture stdlib logging and export via OTLP
export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true

# Export traces, metrics, and logs by default (override with env if needed)
export OTEL_TRACES_EXPORTER="${OTEL_TRACES_EXPORTER:-otlp}"
export OTEL_METRICS_EXPORTER="${OTEL_METRICS_EXPORTER:-otlp}"
export OTEL_LOGS_EXPORTER="${OTEL_LOGS_EXPORTER:-otlp}"

# Start service C (backend), then B, then A. Each runs with its own OTEL_SERVICE_NAME
# so traces look like a distributed system. All inherit OTEL_EXPORTER_OTLP_* from env.

export PORT=8002
export OTEL_SERVICE_NAME=service-c
opentelemetry-instrument python -m app.service_c &
PID_C=$!

export PORT=8001
export OTEL_SERVICE_NAME=service-b
export SERVICE_C_URL=http://127.0.0.1:8002
opentelemetry-instrument python -m app.service_b &
PID_B=$!

export PORT=8000
export OTEL_SERVICE_NAME=service-a
export SERVICE_B_URL=http://127.0.0.1:8001
opentelemetry-instrument python -m app.service_a &
PID_A=$!

# Wait for services to bind
sleep 2

# Run loader in foreground (keeps container alive; triggers A every TELEMETRY_INTERVAL_SECONDS)
export SERVICE_A_URL=http://127.0.0.1:8000
exec python -m app.loader

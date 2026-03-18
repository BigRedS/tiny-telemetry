# Tiny Telemetry

A single Docker image that continuously emits **traces**, **metrics**, and **logs** for testing OpenTelemetry pipelines. It simulates a distributed application with three services (A → B → C) in one container, with optional simulated failures.

- **Traces**: HTTP calls between service-a, service-b, and service-c produce spans that look like a real distributed trace.
- **Metrics**: Auto-instrumentation exposes HTTP client/server metrics.
- **Logs**: Application logs are exported via OTLP when configured.

Runs on Docker, ECS, and Kubernetes. Configuration is via environment variables.

## Build

```bash
docker build -t tiny-telemetry .
```

**CI (GitHub Actions)**  
Pushes to **GitHub Container Registry** on push to the default branch:  
`ghcr.io/<owner>/tiny-telemetry:latest` (and `ghcr.io/<owner>/tiny-telemetry:<sha>`).  
Pull with: `docker pull ghcr.io/<owner>/tiny-telemetry:latest`.  
To use Docker Hub instead, add `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` secrets and switch the workflow to `docker.io` (see [docker/login-action](https://github.com/docker/login-action)).

## Configuration (environment variables)

### Collector (required)

| Variable | Description | Example |
|----------|-------------|---------|
| `OTEL_EXPORTER_OTLP_ENDPOINT` | OTLP endpoint for the collector | `http://collector:4318` |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | `http/protobuf` or `grpc` | `http/protobuf` (default for HTTP) |

Use port **4318** for HTTP and **4317** for gRPC unless your collector differs.

### Telemetry rate

| Variable | Description | Default |
|----------|-------------|---------|
| `TELEMETRY_INTERVAL_SECONDS` | Seconds between each trace (request from loader to service-a) | `5` |

Lower value = more traces/metrics/logs per minute.

### Failures

| Variable | Description | Default |
|----------|-------------|---------|
| `FAILURE_RATE` | Probability (0.0–1.0) that service-c returns an error | `0.1` |

### Optional OTel settings

- Traces, metrics, and logs are exported via OTLP by default when you set `OTEL_EXPORTER_OTLP_ENDPOINT`. Override with `OTEL_TRACES_EXPORTER`, `OTEL_METRICS_EXPORTER`, or `OTEL_LOGS_EXPORTER` (e.g. `none` to disable one).
- `OTEL_EXPORTER_OTLP_HEADERS` — e.g. `Authorization=Bearer token` or API key headers.
- `OTEL_SERVICE_NAME` — overrides default only if you run a single process; the image sets service names per process (service-a, service-b, service-c).

## Run

**Docker**

```bash
docker run --rm \
  -e OTEL_EXPORTER_OTLP_ENDPOINT=http://host.docker.internal:4318 \
  -e OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf \
  -e TELEMETRY_INTERVAL_SECONDS=3 \
  -e FAILURE_RATE=0.2 \
  tiny-telemetry
```

**Docker Compose** (with a collector): see [examples/docker-compose.yaml](examples/docker-compose.yaml). From repo root:

```bash
docker compose -f examples/docker-compose.yaml up --build
```

**Kubernetes / ECS**: see [examples/](examples/) for ready-to-use manifests. Set the same env vars in your pod/task; point `OTEL_EXPORTER_OTLP_ENDPOINT` at your collector. The image has no required volume mounts or ports; it only needs network access to the collector.

**ECS (Fargate)**: [examples/ecs-task-definition.json](examples/ecs-task-definition.json). Replace:

- `YOUR_ACCOUNT_ID`, `YOUR_REGION` in execution/task role ARNs and image URI
- Image: push the built image to ECR and use that URI
- `OTEL_EXPORTER_OTLP_ENDPOINT`: use the hostname of your collector (e.g. an ECS service name in the same cluster, or a load balancer DNS)
- Create log group `/ecs/tiny-telemetry` (or change `awslogs-group`) before running the task

Register and run:

```bash
aws ecs register-task-definition --cli-input-json file://examples/ecs-task-definition.json
aws ecs run-task --cluster YOUR_CLUSTER --task-definition tiny-telemetry --launch-type FARGATE --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

**Kubernetes**: [examples/kubernetes.yaml](examples/kubernetes.yaml). Adjust `OTEL_EXPORTER_OTLP_ENDPOINT` to your collector; then `kubectl apply -f examples/kubernetes.yaml`.

**Other runners** (no example included): the same image and env vars work on **Google Cloud Run**, **Azure Container Instances**, **HashiCorp Nomad**, and **Podman** (e.g. `podman run` or `podman-compose`). Use the Docker run example as a template and set the OTLP endpoint for your environment.

## How it works

- One process runs three instrumented Flask apps (service-a on 8000, service-b on 8001, service-c on 8002) and a loader.
- The loader calls service-a on a timer; service-a calls service-b; service-b calls service-c. Each app uses `opentelemetry-instrument` with a different `OTEL_SERVICE_NAME`, so one trace contains spans from all three “services.”
- Service-c randomly returns 500 based on `FAILURE_RATE`, so you can test error handling and red in traces.
- All telemetry is sent to the configured OTLP endpoint (traces; metrics and logs if enabled via env).

## License

Two-clause BSD. See [LICENSE](LICENSE).

# Examples

Minimal runnable examples for different container runners.

| File | Runner | Notes |
|------|--------|--------|
| [ecs-task-definition.json](ecs-task-definition.json) | AWS ECS (Fargate) | Replace `YOUR_ACCOUNT_ID`, `YOUR_REGION`; push image to ECR; create log group `/ecs/tiny-telemetry`. |
| [docker-compose.yaml](docker-compose.yaml) | Docker Compose | Includes collector. From repo root: `docker compose -f examples/docker-compose.yaml up --build`. |
| [kubernetes.yaml](kubernetes.yaml) | Kubernetes | Point `OTEL_EXPORTER_OTLP_ENDPOINT` at your collector; apply with `kubectl apply -f examples/kubernetes.yaml`. |

The [otel.yaml](otel.yaml) in this folder is used by the Docker Compose stack (collector config).

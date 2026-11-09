# DevOps Observability Platform

An end-to-end observability platform built using **Prometheus, Grafana, Loki, Grafana Alloy, Jaeger, OpenTelemetry, Docker, and Python Flask**.

This project demonstrates how to collect, monitor, visualize, and correlate application metrics, logs, and distributed traces in a containerized environment.

## Architecture

The platform implements the three pillars of observability:

- **Metrics:** Prometheus collects application metrics.
- **Logs:** Grafana Alloy collects application logs and forwards them to Loki.
- **Traces:** OpenTelemetry instruments the Flask application and exports distributed traces to Jaeger.
- **Visualization:** Grafana provides dashboards for metrics, logs, and traces.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python Flask | Sample application |
| Prometheus | Metrics collection |
| Grafana | Visualization and dashboards |
| Loki | Log aggregation |
| Grafana Alloy | Log collection and forwarding |
| Jaeger | Distributed tracing |
| OpenTelemetry | Application instrumentation |
| Docker Compose | Container orchestration |

## Project Structure

```text
devops-observability-project/
├── alloy/
│   └── config.alloy
├── app/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── grafana/
│   ├── provisioning/
│   │   └── datasources/
│   │       └── datasources.yml
│   └── dashboards/
├── loki/
│   └── local-config.yaml
├── prometheus/
│   └── prometheus.yml
├── logs/
├── docker-compose.yml
└── README.md
```

## Features

- Containerized Flask application.
- Application request count and response-time metrics.
- Centralized application log collection.
- Distributed tracing using OpenTelemetry and Jaeger.
- Grafana dashboards for monitoring metrics, logs, and traces.
- Docker Compose-based deployment.

## Deployment Instructions

### Prerequisites

- Docker
- Docker Compose
- Git

### Clone the repository

```bash
git clone https://github.com/ParvathiSKallanagoudar/devops-observability-platform.git

cd devops-observability-platform
```

### Start the platform

```bash
docker compose up -d --build
```

### Check running containers

```bash
docker compose ps
```

### Generate application traffic

```bash
curl http://localhost:8001/

curl http://localhost:8001/health

curl http://localhost:8001/work

curl http://localhost:8001/metrics
```

## Access the Services

| Service | URL |
|---|---|
| Flask Application | http://localhost:8001 |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 |
| Loki | http://localhost:3100 |
| Jaeger | http://localhost:16686 |
| Grafana Alloy | http://localhost:12345 |

## Project Screenshots

### 1. Grafana Observability Dashboard

![Grafana Dashboard](screenshots/Screenshot%20(273).png)

### 2. Grafana Metrics, Logs and Traces

![Grafana Metrics and Logs](screenshots/Screenshot%20(274).png)

The dashboard demonstrates application request metrics, request rates, average response time, centralized application logs, and Jaeger trace duration.

## Verification

The platform was tested by:

1. Generating application requests through Flask endpoints.
2. Verifying application metrics in Prometheus.
3. Confirming log collection through Alloy and Loki.
4. Verifying distributed traces in Jaeger.
5. Creating Grafana panels for request count, request rate, average response time, application logs, and trace search.

## Conclusion

This project demonstrates an end-to-end observability workflow using open-source DevOps tools. It provides practical experience with metrics monitoring, centralized logging, distributed tracing, containerization, and dashboard visualization.

**Author:** Parvathi S. Kallanagoudar

**GitHub:** https://github.com/ParvathiSKallanagoudar

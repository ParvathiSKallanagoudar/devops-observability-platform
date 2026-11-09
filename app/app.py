import logging
import os
import random
import time

from flask import Flask, jsonify, request
from prometheus_client import Counter, Histogram, generate_latest
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

app = Flask(__name__)

# -------------------------------
# Logging configuration
# -------------------------------

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("observability-app")

# -------------------------------
# OpenTelemetry tracing
# -------------------------------

resource = Resource.create({
    "service.name": "observability-demo-app"
})

provider = TracerProvider(resource=resource)

otlp_exporter = OTLPSpanExporter(
    endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://jaeger:4317"),
    insecure=True
)

provider.add_span_processor(
    BatchSpanProcessor(otlp_exporter)
)

trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

# -------------------------------
# Prometheus metrics
# -------------------------------

REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total number of application requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "app_request_duration_seconds",
    "Application request duration in seconds",
    ["endpoint"]
)

# -------------------------------
# Application routes
# -------------------------------

@app.route("/")
def home():
    with tracer.start_as_current_span("home-request"):
        logger.info("Home endpoint accessed")

        REQUEST_COUNT.labels(
            method="GET",
            endpoint="/",
            status="200"
        ).inc()

        return jsonify({
            "message": "Welcome to the Observability Demo Application",
            "status": "running"
        })


@app.route("/health")
def health():
    with tracer.start_as_current_span("health-check"):
        logger.info("Health check requested")

        REQUEST_COUNT.labels(
            method="GET",
            endpoint="/health",
            status="200"
        ).inc()

        return jsonify({"status": "healthy"})


@app.route("/work")
def work():
    with tracer.start_as_current_span("work-request"):
        start_time = time.time()

        logger.info("Work endpoint started")

        # Simulate application processing
        time.sleep(random.uniform(0.1, 0.8))

        duration = time.time() - start_time

        REQUEST_LATENCY.labels(endpoint="/work").observe(duration)

        REQUEST_COUNT.labels(
            method="GET",
            endpoint="/work",
            status="200"
        ).inc()

        logger.info("Work endpoint completed in %.3f seconds", duration)

        return jsonify({
            "message": "Work completed successfully",
            "processing_time_seconds": round(duration, 3)
        })


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {
        "Content-Type": "text/plain; version=0.0.4"
    }


@app.errorhandler(404)
def not_found(error):
    logger.warning("Endpoint not found: %s", request.path)

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint="unknown",
        status="404"
    ).inc()

    return jsonify({"error": "Endpoint not found"}), 404


if __name__ == "__main__":
    logger.info("Starting Observability Demo Application")

    app.run(
        host="0.0.0.0",
        port=8000
    )
"""Prometheus metrics instrumentation for FastAPI schema architect.

Exports metrics on /metrics endpoint in Prometheus format.
Metrics include:
- Request count/duration/errors by endpoint
- Schema registry operations (register, validate, publish)
- Feature extraction metrics
- Resource usage (CPU, memory)
"""

from prometheus_client import Counter, Histogram, Gauge, generate_latest
from fastapi import Request
from typing import Callable
import time
import psutil
import os

# Request metrics
request_count = Counter(
    'schema_architect_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

request_duration_seconds = Histogram(
    'schema_architect_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint'],
    buckets=(0.01, 0.05, 0.1, 0.5, 1.0, 2.5, 5.0)
)

# Schema registry metrics
schema_registrations_total = Counter(
    'schema_architect_registrations_total',
    'Total schemas registered',
    ['schema_type', 'status']
)

schema_validations_total = Counter(
    'schema_architect_validations_total',
    'Total schema validations',
    ['status']  # valid/invalid
)

validation_duration_seconds = Histogram(
    'schema_architect_validation_duration_seconds',
    'Schema validation latency',
    buckets=(0.001, 0.005, 0.01, 0.05, 0.1, 0.5)
)

publish_hooks_total = Counter(
    'schema_architect_publish_hooks_total',
    'Total publish hooks executed',
    ['status']  # success/failure/timeout
)

publish_hooks_duration_seconds = Histogram(
    'schema_architect_publish_hooks_duration_seconds',
    'Publish hook latency',
    buckets=(0.1, 0.5, 1.0, 5.0, 10.0)
)

# Feature engineering metrics
feature_extractions_total = Counter(
    'schema_architect_feature_extractions_total',
    'Total feature extractions',
    ['featurizer_type', 'status']
)

feature_extraction_duration_seconds = Histogram(
    'schema_architect_feature_extraction_duration_seconds',
    'Feature extraction latency',
    ['featurizer_type'],
    buckets=(0.01, 0.05, 0.1, 0.5, 1.0, 5.0)
)

feast_query_duration_seconds = Histogram(
    'schema_architect_feast_query_duration_seconds',
    'Feast feature store query latency',
    buckets=(0.01, 0.05, 0.1, 0.25, 0.5)
)

# Resource metrics
cpu_usage_percent = Gauge(
    'schema_architect_cpu_usage_percent',
    'CPU usage percentage'
)

memory_usage_percent = Gauge(
    'schema_architect_memory_usage_percent',
    'Memory usage percentage'
)

disk_usage_percent = Gauge(
    'schema_architect_disk_usage_percent',
    'Disk usage percentage',
    ['mount_point']
)

# Process metrics
process_uptime_seconds = Gauge(
    'schema_architect_process_uptime_seconds',
    'Process uptime in seconds'
)

active_requests = Gauge(
    'schema_architect_active_requests',
    'Currently active HTTP requests'
)


def update_resource_metrics() -> None:
    """Update system resource metrics."""
    try:
        cpu_usage_percent.set(psutil.cpu_percent(interval=0.1))
        memory_usage_percent.set(psutil.virtual_memory().percent)
        
        # Disk usage for root
        disk_usage = psutil.disk_usage('/')
        disk_usage_percent.labels(mount_point='/').set(disk_usage.percent)
    except Exception as e:
        # Log but don't fail if metrics collection fails
        print(f"Error collecting resource metrics: {e}")


async def metrics_middleware(request: Request, call_next: Callable):
    """Middleware to record request metrics."""
    active_requests.inc()
    start_time = time.time()
    
    try:
        response = await call_next(request)
        status_code = response.status_code
    except Exception as e:
        status_code = 500
        raise
    finally:
        active_requests.dec()
        duration = time.time() - start_time
        
        # Normalize endpoint path (remove IDs for cardinality)
        endpoint = request.url.path
        if endpoint.startswith('/schemas/'):
            endpoint = '/schemas/{schema_id}'
        elif endpoint.startswith('/validate'):
            endpoint = '/validate'
        
        request_count.labels(
            method=request.method,
            endpoint=endpoint,
            status=status_code
        ).inc()
        
        request_duration_seconds.labels(
            method=request.method,
            endpoint=endpoint
        ).observe(duration)
    
    return response


def get_metrics() -> str:
    """Return Prometheus metrics in text format."""
    update_resource_metrics()
    return generate_latest().decode('utf-8')

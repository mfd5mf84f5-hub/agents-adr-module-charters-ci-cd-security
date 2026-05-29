"""OpenTelemetry configuration for distributed tracing.

Provides foundation for distributed tracing across microservices.
Phase 2: Basic setup with Jaeger exporter placeholder.
Phase 3: Production deployment with APM.
"""

from opentelemetry import trace, metrics
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
import os


def init_tracing(service_name: str = 'schema-architect',
                 jaeger_host: str = None,
                 jaeger_port: int = 6831,
                 enabled: bool = True) -> TracerProvider:
    """Initialize OpenTelemetry tracing.
    
    Args:
        service_name: Name of this service
        jaeger_host: Jaeger agent host (default: from env or localhost)
        jaeger_port: Jaeger agent port (default: 6831)
        enabled: Whether to enable tracing (default: True)
    
    Returns:
        TracerProvider instance
    
    Usage:
        tracer_provider = init_tracing()
        trace.set_tracer_provider(tracer_provider)
        FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer_provider)
    """
    if not enabled:
        return trace.NoOpTracerProvider()
    
    # Use environment variables if provided
    jaeger_host = jaeger_host or os.getenv('JAEGER_AGENT_HOST', 'localhost')
    jaeger_port = int(os.getenv('JAEGER_AGENT_PORT', jaeger_port))
    
    # Create Jaeger exporter
    jaeger_exporter = JaegerExporter(
        agent_host_name=jaeger_host,
        agent_port=jaeger_port,
    )
    
    # Create trace provider with resource
    resource = Resource.create({SERVICE_NAME: service_name})
    tracer_provider = TracerProvider(resource=resource)
    
    # Add Jaeger exporter
    tracer_provider.add_span_processor(
        BatchSpanProcessor(jaeger_exporter)
    )
    
    return tracer_provider


def instrument_app(app, tracer_provider: TracerProvider = None):
    """Instrument FastAPI app for tracing.
    
    Args:
        app: FastAPI application instance
        tracer_provider: TracerProvider (uses global if not specified)
    """
    if tracer_provider:
        trace.set_tracer_provider(tracer_provider)
    
    # Instrument FastAPI
    FastAPIInstrumentor.instrument_app(app)
    
    # Instrument outgoing HTTP requests
    RequestsInstrumentor().instrument()
    HTTPXClientInstrumentor().instrument()


def instrument_database(engine):
    """Instrument database for tracing.
    
    Args:
        engine: SQLAlchemy engine instance
    """
    SQLAlchemyInstrumentor().instrument(engine=engine)


def get_tracer(name: str) -> trace.Tracer:
    """Get a tracer for the current service.
    
    Usage:
        tracer = get_tracer(__name__)
        with tracer.start_as_current_span('operation_name'):
            # Do work
            pass
    """
    return trace.get_tracer(name)

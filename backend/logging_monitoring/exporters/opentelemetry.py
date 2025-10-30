"""
OpenTelemetry exporter

Note: This is a mock implementation for development.
In production, use opentelemetry-api and opentelemetry-sdk libraries.
"""

from typing import Dict, Any, Optional
from datetime import datetime


class OpenTelemetryExporter:
    """
    OpenTelemetry exporter for traces, metrics, and logs
    
    Mock implementation for development. In production, integrate with
    opentelemetry-api and opentelemetry-sdk:
    
    from opentelemetry import trace, metrics
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    """
    
    def __init__(
        self,
        endpoint: str = "http://localhost:4317",
        service_name: str = "selamai-trading",
        headers: Optional[Dict[str, str]] = None,
    ):
        self.endpoint = endpoint
        self.service_name = service_name
        self.headers = headers or {}
        self.enabled = False
        self.spans = []
        self.metrics = []
    
    def enable(self) -> None:
        """Enable OpenTelemetry exporter"""
        self.enabled = True
        print(f"[OpenTelemetry Exporter] Enabled for service: {self.service_name}")
        print(f"[OpenTelemetry Exporter] Endpoint: {self.endpoint}")
        print("[OpenTelemetry Exporter] Note: This is a mock implementation")
        print("[OpenTelemetry Exporter] For production, install:")
        print("  pip install opentelemetry-api opentelemetry-sdk")
        print("  pip install opentelemetry-exporter-otlp")
    
    def start_span(self, name: str, attributes: Optional[Dict[str, Any]] = None) -> "MockSpan":
        """Start a new trace span"""
        span = MockSpan(name, attributes or {})
        self.spans.append(span)
        return span
    
    def record_metric(self, name: str, value: float, attributes: Optional[Dict[str, Any]] = None) -> None:
        """Record a metric"""
        self.metrics.append({
            "name": name,
            "value": value,
            "attributes": attributes or {},
            "timestamp": datetime.utcnow(),
        })
    
    def get_stats(self) -> Dict[str, Any]:
        """Get exporter statistics"""
        return {
            "enabled": self.enabled,
            "service_name": self.service_name,
            "endpoint": self.endpoint,
            "spans_recorded": len(self.spans),
            "metrics_recorded": len(self.metrics),
        }


class MockSpan:
    """Mock span for development"""
    
    def __init__(self, name: str, attributes: Dict[str, Any]):
        self.name = name
        self.attributes = attributes
        self.start_time = datetime.utcnow()
        self.end_time: Optional[datetime] = None
        self.status = "OK"
    
    def set_attribute(self, key: str, value: Any) -> None:
        """Set span attribute"""
        self.attributes[key] = value
    
    def set_status(self, status: str) -> None:
        """Set span status"""
        self.status = status
    
    def end(self) -> None:
        """End the span"""
        self.end_time = datetime.utcnow()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.status = "ERROR"
            self.set_attribute("error.type", exc_type.__name__)
            self.set_attribute("error.message", str(exc_val))
        self.end()


def get_opentelemetry_exporter(
    enabled: bool = False,
    endpoint: str = "http://localhost:4317",
    service_name: str = "selamai-trading",
) -> OpenTelemetryExporter:
    """
    Get OpenTelemetry exporter instance
    
    For production use, install OpenTelemetry packages:
    pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp
    
    Then use:
    from opentelemetry import trace
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    """
    exporter = OpenTelemetryExporter(
        endpoint=endpoint,
        service_name=service_name,
    )
    
    if enabled:
        exporter.enable()
        print("\n" + "="*60)
        print("OPENTELEMETRY INTEGRATION SETUP")
        print("="*60)
        print("\nFor production, install OpenTelemetry packages:")
        print("  pip install opentelemetry-api opentelemetry-sdk")
        print("  pip install opentelemetry-exporter-otlp")
        print("\nExample usage:")
        print("  from opentelemetry import trace")
        print("  from opentelemetry.sdk.trace import TracerProvider")
        print("  from opentelemetry.sdk.trace.export import BatchSpanProcessor")
        print("  from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter")
        print("  ")
        print("  # Setup tracer")
        print("  trace.set_tracer_provider(TracerProvider())")
        print("  tracer = trace.get_tracer(__name__)")
        print("  ")
        print("  # Add exporter")
        print("  otlp_exporter = OTLPSpanExporter(endpoint='localhost:4317')")
        print("  span_processor = BatchSpanProcessor(otlp_exporter)")
        print("  trace.get_tracer_provider().add_span_processor(span_processor)")
        print("  ")
        print("  # Use in code")
        print("  with tracer.start_as_current_span('operation'):")
        print("      # Your code here")
        print("      pass")
        print("="*60 + "\n")
    
    return exporter

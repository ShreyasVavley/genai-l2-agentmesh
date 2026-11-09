import time
import uuid
from typing import Dict, Any, List

class TraceSpan:
    def __init__(self, trace_id: str, span_name: str, node_name: str, parent_id: str = None):
        self.span_id = str(uuid.uuid4())[:8]
        self.trace_id = trace_id
        self.span_name = span_name
        self.node_name = node_name
        self.parent_id = parent_id
        self.start_time = time.time()
        self.end_time = None
        self.duration_ms = 0.0
        self.attributes: Dict[str, Any] = {}
        self.events: List[Dict[str, Any]] = []

    def set_attribute(self, key: str, value: Any):
        self.attributes[key] = value

    def add_event(self, name: str, payload: Dict[str, Any] = None):
        self.events.append({
            "name": name,
            "timestamp": time.time(),
            "payload": payload or {}
        })

    def finish(self):
        self.end_time = time.time()
        self.duration_ms = round((self.end_time - self.start_time) * 1000, 2)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "span_id": self.span_id,
            "trace_id": self.trace_id,
            "span_name": self.span_name,
            "node_name": self.node_name,
            "duration_ms": self.duration_ms,
            "attributes": self.attributes,
            "events": self.events
        }

class AgentTracer:
    """OpenTelemetry-compatible trace collector for Agentic systems."""
    def __init__(self):
        self.traces: Dict[str, List[TraceSpan]] = {}

    def start_span(self, trace_id: str, span_name: str, node_name: str) -> TraceSpan:
        span = TraceSpan(trace_id, span_name, node_name)
        if trace_id not in self.traces:
            self.traces[trace_id] = []
        self.traces[trace_id].append(span)
        return span

    def get_trace(self, trace_id: str) -> List[Dict[str, Any]]:
        spans = self.traces.get(trace_id, [])
        return [s.to_dict() for s in spans]

    def get_summary_metrics(self) -> Dict[str, Any]:
        total_spans = sum(len(spans) for spans in self.traces.values())
        avg_latency = 0.0
        durations = [s.duration_ms for spans in self.traces.values() for s in spans if s.duration_ms > 0]
        if durations:
            avg_latency = round(sum(durations) / len(durations), 2)
        return {
            "total_recorded_traces": len(self.traces),
            "total_spans": total_spans,
            "average_span_latency_ms": avg_latency
        }

tracer = AgentTracer()

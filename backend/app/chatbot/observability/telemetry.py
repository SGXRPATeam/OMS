import time
import hashlib
from typing import Optional, List
from app.chatbot.core.config import chatbot_settings
from app.chatbot.core.logging import get_logger

logger = get_logger(__name__)

_tracer = None
_meter = None


def get_tracer():
    return _tracer


def get_meter():
    return _meter


def _mask_user_id(user_id: str) -> str:
    return "masked_user_" + hashlib.sha256(user_id.encode()).hexdigest()[:8]


def _mask_query(query: str) -> str:
    return "masked_query_hash_" + hashlib.sha256(query.encode()).hexdigest()[:7]


def setup_telemetry(app=None):
    global _tracer, _meter

    if not chatbot_settings.otel_enabled:
        logger.info("otel_disabled")
        _tracer = _NoopTracer()
        return

    try:
        from opentelemetry import trace, metrics
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
        from opentelemetry.sdk.metrics import MeterProvider
        from opentelemetry.sdk.metrics.export import ConsoleMetricExporter, PeriodicExportingMetricReader
        from opentelemetry.sdk.resources import Resource

        resource = Resource.create({
            "service.name":           chatbot_settings.otel_service_name,
            "service.version":        chatbot_settings.app_version,
            "deployment.environment": chatbot_settings.app_env,
            "cloud.provider":         "local",
            "k8s.cluster.name":       "local-dev",
            "k8s.namespace.name":     "oms-chatbot",
        })

        try:
            from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
            span_exporter = OTLPSpanExporter(
                endpoint=chatbot_settings.otel_exporter_otlp_endpoint,
                insecure=True,
            )
        except Exception:
            span_exporter = ConsoleSpanExporter()

        trace_provider = TracerProvider(resource=resource)
        trace_provider.add_span_processor(BatchSpanProcessor(span_exporter))
        trace.set_tracer_provider(trace_provider)
        _tracer = trace.get_tracer("otel.ai.observability", schema_url="https://opentelemetry.io/schemas/1.21.0")

        try:
            from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
            metric_exporter = OTLPMetricExporter(
                endpoint=chatbot_settings.otel_exporter_otlp_endpoint,
                insecure=True,
            )
        except Exception:
            metric_exporter = ConsoleMetricExporter()

        metric_reader = PeriodicExportingMetricReader(metric_exporter, export_interval_millis=30000)
        meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
        metrics.set_meter_provider(meter_provider)
        _meter = metrics.get_meter("otel.ai.observability", "0.1.0")

        _register_metrics(_meter)

        if app:
            from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
            FastAPIInstrumentor.instrument_app(app)

        logger.info("otel_configured", service=chatbot_settings.otel_service_name)

    except ImportError as e:
        logger.warning("otel_setup_skipped_import_error", reason=str(e))
        _tracer = _NoopTracer()


_counters = {}
_histograms = {}


def _register_metrics(meter):
    global _counters, _histograms

    _counters["llm_requests_total"] = meter.create_counter("llm.requests.total", unit="1")
    _counters["llm_errors_total"] = meter.create_counter("llm.errors.total", unit="1")
    _counters["guardrail_blocks_total"] = meter.create_counter("guardrail.blocks.total", unit="1")
    _counters["pii_detections_total"] = meter.create_counter("pii.detections.total", unit="1")
    _counters["hallucinations_total"] = meter.create_counter("quality.hallucinations.total", unit="1")
    _counters["handoffs_total"] = meter.create_counter("handoff.total", unit="1")
    _counters["tokens_total"] = meter.create_counter("llm.tokens.total", unit="1")

    _histograms["llm_latency"] = meter.create_histogram("llm.latency.ms", unit="ms")
    _histograms["retrieval_latency"] = meter.create_histogram("rag.retrieval.latency.ms", unit="ms")
    _histograms["total_latency"] = meter.create_histogram("request.total.latency.ms", unit="ms")
    _histograms["groundedness"] = meter.create_histogram("quality.groundedness.score", unit="1")
    _histograms["cost_usd"] = meter.create_histogram("cost.estimated.usd", unit="usd")


def _inc(counter_name: str, value: int = 1, attributes: dict = None):
    c = _counters.get(counter_name)
    if c:
        c.add(value, attributes or {})


def _record(histogram_name: str, value: float, attributes: dict = None):
    h = _histograms.get(histogram_name)
    if h:
        h.record(value, attributes or {})


class _NoopSpan:
    def set_attribute(self, *a, **kw): pass
    def set_status(self, *a, **kw): pass
    def record_exception(self, *a, **kw): pass
    def add_event(self, *a, **kw): pass
    def __enter__(self): return self
    def __exit__(self, *a): pass


class _NoopTracer:
    def start_as_current_span(self, *a, **kw):
        from contextlib import contextmanager
        @contextmanager
        def _cm():
            yield _NoopSpan()
        return _cm()

    def start_span(self, *a, **kw):
        return _NoopSpan()


class AISpanBuilder:

    def __init__(self):
        self._span = None
        self._start_ts: float = 0.0

    def start(self, event_name, trace_id, request_id, user_id, tenant_id,
              request_type="chat_message", request_channel="web"):
        tracer = get_tracer()
        if tracer is None or isinstance(tracer, _NoopTracer):
            self._span = _NoopSpan()
            self._start_ts = time.monotonic()
            return self

        self._start_ts = time.monotonic()
        span_ctx = tracer.start_as_current_span(event_name)
        self._span = span_ctx.__enter__()

        self._span.set_attribute("trace.id", trace_id)
        self._span.set_attribute("request.id", request_id)
        self._span.set_attribute("user.id", _mask_user_id(user_id))
        self._span.set_attribute("tenant.id", tenant_id)
        self._span.set_attribute("request.type", request_type)
        self._span.set_attribute("request.channel", request_channel)
        return self

    def set_guardrail(self, passed, pii_detected, pii_types,
                     injection_detected=False, toxicity_detected=False):
        if not self._span:
            return
        self._span.set_attribute("policy.guardrail.status", "passed" if passed else "blocked")
        self._span.set_attribute("policy.pii_detected", pii_detected)
        self._span.set_attribute("policy.injection_detected", injection_detected)
        self._span.set_attribute("policy.toxicity_detected", toxicity_detected)
        if pii_detected:
            _inc("pii_detections_total")
        if not passed:
            _inc("guardrail_blocks_total")

    def set_workflow(self, intent_code, intent_label, response_mode, confidence,
                     steps_count=9, status="completed"):
        if not self._span:
            return
        self._span.set_attribute("workflow.intent_code", intent_code)
        self._span.set_attribute("workflow.intent_label", intent_label)
        self._span.set_attribute("workflow.response_mode", response_mode)
        self._span.set_attribute("workflow.confidence", round(confidence, 4))
        self._span.set_attribute("workflow.status", status)

    def set_llm(self, model, provider="ollama", temperature=0.1, prompt_tokens=0,
                completion_tokens=0, total_tokens=0, llm_latency_ms=0,
                prompt_version="v1.0", prompt_template_id="oms_chatbot_main"):
        if not self._span:
            return
        self._span.set_attribute("llm.model", model)
        self._span.set_attribute("llm.provider", provider)
        self._span.set_attribute("performance.llm_latency_ms", llm_latency_ms)
        _inc("llm_requests_total", attributes={"llm.model": model})
        _inc("tokens_total", value=total_tokens, attributes={"llm.model": model})
        _record("llm_latency", llm_latency_ms, attributes={"llm.model": model})

    def set_rag(self, query, docs_retrieved, docs_used, top_score=0.0,
                lowest_used_score=0.0, retrieval_latency_ms=0,
                vector_store="postgresql_keyword", embedding_model="disabled"):
        if not self._span:
            return
        self._span.set_attribute("rag.documents_retrieved", docs_retrieved)
        self._span.set_attribute("rag.documents_used", docs_used)
        self._span.set_attribute("performance.retrieval_latency_ms", retrieval_latency_ms)
        _record("retrieval_latency", retrieval_latency_ms)

    def set_quality(self, groundedness_score, hallucination_flag,
                    answer_relevance_score=0.0, toxicity_score=0.0, pii_flag=False):
        if not self._span:
            return
        self._span.set_attribute("quality.groundedness_score", round(groundedness_score, 4))
        self._span.set_attribute("quality.hallucination_flag", hallucination_flag)
        self._span.set_attribute("quality.pii_flag", pii_flag)
        _record("groundedness", groundedness_score)
        if hallucination_flag:
            _inc("hallucinations_total")

    def set_cost(self, total_tokens, model="ollama_local"):
        if not self._span:
            return
        self._span.set_attribute("cost.estimated_usd", 0.0)
        self._span.set_attribute("cost.total_tokens", total_tokens)
        _record("cost_usd", 0.0, attributes={"llm.model": model})

    def finish(self, gateway_latency_ms, total_latency_ms,
               error: Optional[Exception] = None, requires_human: bool = False):
        if not self._span:
            return
        self._span.set_attribute("performance.total_latency_ms", total_latency_ms)
        self._span.set_attribute("alert.triggered", requires_human or error is not None)
        if error:
            try:
                from opentelemetry.trace import StatusCode
                self._span.record_exception(error)
                self._span.set_status(StatusCode.ERROR, str(error))
            except Exception:
                pass
            _inc("llm_errors_total")
        _record("total_latency", total_latency_ms)
        if requires_human:
            _inc("handoffs_total")

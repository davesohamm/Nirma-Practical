"""
Prometheus Metrics Middleware for FastAPI.
Tracks request count, latency, error rate, predictions, inference time, and active users.
"""

import time
import threading
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

# ─── Prometheus Metrics ──────────────────────────────────────────────────────

# HTTP metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"],
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
)

ERROR_COUNT = Counter(
    "http_errors_total",
    "Total HTTP error responses (4xx/5xx)",
    ["method", "endpoint", "status"]
)

# ML-specific metrics
PREDICTION_COUNT = Counter(
    "predictions_total",
    "Total predictions made",
    ["model_version"]
)

INFERENCE_TIME = Histogram(
    "model_inference_seconds",
    "Model inference time in seconds",
    ["model_version"],
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0]
)

ACTIVE_USERS = Gauge(
    "active_users_gauge",
    "Currently active users (seen in last 5 minutes)"
)

PREDICTIONS_TODAY = Counter(
    "predictions_today_total",
    "Predictions made today (resets via relabel)"
)

# ─── Active User Tracker ────────────────────────────────────────────────────
# Tracks unique user IDs that made authenticated requests in the last 5 min

_active_users_lock = threading.Lock()
_active_users: dict[str, float] = {}  # user_id -> last_seen_timestamp
ACTIVE_WINDOW_SECONDS = 300  # 5 minutes


def track_active_user(user_id: str):
    """Record a user as active (called from auth-protected routes)."""
    now = time.time()
    with _active_users_lock:
        _active_users[user_id] = now
        _cleanup_and_update_gauge(now)


def _cleanup_and_update_gauge(now: float):
    """Remove stale users and update the Prometheus gauge."""
    cutoff = now - ACTIVE_WINDOW_SECONDS
    stale = [uid for uid, ts in _active_users.items() if ts < cutoff]
    for uid in stale:
        del _active_users[uid]
    ACTIVE_USERS.set(len(_active_users))


class PrometheusMiddleware(BaseHTTPMiddleware):
    """Middleware that records Prometheus metrics for every request."""

    async def dispatch(self, request: Request, call_next):
        # Skip metrics endpoint itself to avoid recursion
        if request.url.path == "/metrics":
            # Refresh active users gauge on every scrape
            with _active_users_lock:
                _cleanup_and_update_gauge(time.time())
            return await call_next(request)

        method = request.method
        # Normalize path to avoid cardinality explosion
        endpoint = self._normalize_path(request.url.path)

        # Track active users from Authorization header
        auth_header = request.headers.get("authorization", "")
        if auth_header.startswith("Bearer "):
            try:
                from api.auth.jwt_handler import decode_access_token
                token = auth_header.split(" ", 1)[1]
                payload = decode_access_token(token)
                user_id = payload.get("sub")
                if user_id:
                    track_active_user(user_id)
            except Exception:
                pass

        start_time = time.time()
        response = await call_next(request)
        elapsed = time.time() - start_time

        status_code = str(response.status_code)

        # Record metrics
        REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status_code).inc()
        REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(elapsed)

        if response.status_code >= 400:
            ERROR_COUNT.labels(method=method, endpoint=endpoint, status=status_code).inc()

        return response

    def _normalize_path(self, path: str) -> str:
        """Normalize request paths to prevent label cardinality explosion."""
        # Group parameterized paths
        parts = path.strip("/").split("/")
        if len(parts) > 2:
            return "/" + "/".join(parts[:2])
        return path


def metrics_endpoint():
    """Return Prometheus metrics in text format."""
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

from fastapi import FastAPI, Request
from prometheus_client import Counter, Histogram, make_asgi_app
import time

app = FastAPI()

# Metrics
REQUEST_COUNT = Counter(
    "app_request_count", "Total HTTP requests", ["method", "endpoint", "http_status"]
)
REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds", "Request latency seconds", ["endpoint"]
)

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    latency = time.time() - start
    endpoint = request.url.path
    REQUEST_LATENCY.labels(endpoint=endpoint).observe(latency)
    REQUEST_COUNT.labels(method=request.method, endpoint=endpoint, http_status=str(response.status_code)).inc()
    return response

@app.get("/")
def read_root():
    return {"message": "Hello, Observability World!"}

# Mount the Prometheus ASGI app at /metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

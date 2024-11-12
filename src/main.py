# src/main.py

from fastapi import FastAPI, Request
from src.query.query_service import query_router  # Importing routers from query module
from src.utils.db_utils import get_db_connection
from src.utils.log_utils import setup_logger
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Histogram

app = FastAPI()

# Initialize Prometheus metrics
REQUEST_COUNTER = Counter("http_request_count_total", "Total number of HTTP requests", ["method", "endpoint"])
REQUEST_LATENCY = Histogram("http_request_duration_in_seconds", "Latency of HTTP requests", ["method", "endpoint"])

# Include routers for different endpoints
app.include_router(query_router, prefix="/query", tags=["Query Service"])

Instrumentator().instrument(app).expose(app, endpoint="/metrics")


#@app.middleware("http")
async def add_metrics_middleware(request: Request, call_next):
    """Middleware to track the request count and request latency."""
    method = request.method
    endpoint = request.url.path
    REQUEST_COUNTER.labels(method=method, endpoint=endpoint).inc()

    with REQUEST_LATENCY.labels(method=method, endpoint=endpoint).time():
        response = await call_next(request)
    #response = await call_next(request)
    return response


@app.get("/health")
async def health_check():
    return {"status": "ok"}


# Initialize logger
logger = setup_logger("main")


@app.on_event("startup")
async def startup_event():
    # Startup logic, such as initializing a database connection
    db = get_db_connection()
    logger.info("Database connection established.")


@app.on_event("shutdown")
async def shutdown_event():
    # Shutdown logic, if any
    logger.info("Shutting down application.")


if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

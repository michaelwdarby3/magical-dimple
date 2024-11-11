from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.query.retrieve_data import get_query_embedding, find_similar_embeddings, fetch_records
from src.query.rag_pipeline import generate_rag_response
from src.utils.log_utils import setup_logger
import redis
import json
from prometheus_client import Counter, Histogram

# Initialize Redis client
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Define the query router
query_router = APIRouter()

# Prometheus metrics for RAG endpoint
RAG_REQUESTS = Counter("rag_requests_total", "Total RAG requests", ["status"])
RAG_REQUEST_LATENCY = Histogram("rag_request_duration_seconds", "Latency of RAG requests")

# Set up logger for this service
logger = setup_logger("query_service")


class QueryRequest(BaseModel):
    query: str
    top_k: int = 5
    max_length: int = 1000
    min_length: int = 1
    product_name: str = None
    product_type: str = None


def cache_response(query_key, response):
    """Cache response in Redis with an expiration time."""
    redis_client.set(query_key, json.dumps(response), ex=3600)  # Cache for 1 hour


def get_cached_response(query_key):
    """Retrieve cached response from Redis if available."""
    cached_response = redis_client.get(query_key)
    if cached_response:
        return json.loads(cached_response)
    return None


@query_router.post("/rag")
async def rag_query(request: QueryRequest):
    """
    Endpoint to perform Retriever-Augmented Generation based on the input text.
    """
    with RAG_REQUEST_LATENCY.time():  # Measure request latency
        try:
            result = generate_rag_response(
                query=request.query,
                top_k=request.top_k,
                product_name=request.product_name,
                product_type=request.product_type,
                max_length=request.max_length,
                min_length=request.min_length
            )
            RAG_REQUESTS.labels(status="success").inc()
            return {"response": result['response'], "records": result['records']}

        except Exception as e:
            RAG_REQUESTS.labels(status="error").inc()
            logger.error(f"RAG query failed: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

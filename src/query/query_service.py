from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.query.retrieve_data import get_query_embedding, find_similar_embeddings, fetch_records
from src.query.rag_pipeline import generate_rag_response
from src.utils.log_utils import setup_logger
import redis
import json

# Initialize Redis client
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Define the query router
query_router = APIRouter()

# Set up logger for this service
logger = setup_logger("query_service")

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5
    max_length: int = 50
    min_length: int = 5

class RAGRequest(BaseModel):
    input_text: str  # Define the input text as part of a Pydantic model

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
async def rag_query(request: RAGRequest):  # Use the RAGRequest model
    """
    Endpoint to perform Retriever-Augmented Generation based on the input text.
    """
    try:
        response = generate_rag_response(request.input_text)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@query_router.post("/query")
async def query_similar_records(request: QueryRequest):
    """Asynchronous endpoint to retrieve similar records."""
    query_embedding = await get_query_embedding(request.query)
    matched_ids = await find_similar_embeddings(query_embedding, request.top_k)
    results = await fetch_records(matched_ids)
    return results

@query_router.post("/rag_response")
async def retrieve_and_generate_response(request: QueryRequest):
    """Enhanced RAG endpoint with detailed logging."""

    logger.info("Received RAG hit")
    logger.warning("RAG caching disabled")

    query_key = f"{request.query}:{request.top_k}:{request.max_length}:{request.min_length}"
    cached_response = get_cached_response(query_key)

    if cached_response:
        logger.info("Cache hit for query", extra={"query": request.query})
        return cached_response

    request_info = {"query": request.query, "top_k": request.top_k}
    logger.info("Cache miss: Generating RAG response", extra=request_info)

    try:
        response = await generate_rag_response(request.query, request.top_k, request.max_length, request.min_length)
        logger.info("RAG response generated successfully", extra={"response_length": len(response.get("response", ""))})
        cache_response(query_key, response)
        return response
    except Exception as e:
        logger.error("Error in RAG pipeline", extra={"error": str(e), **request_info})
        raise HTTPException(status_code=500, detail="Error generating RAG response.")

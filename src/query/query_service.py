from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.query.retrieve_data import get_query_embedding, find_similar_embeddings, fetch_records
from src.query.rag_pipeline import generate_rag_response
from src.utils.log_utils import setup_logger
from prometheus_fastapi_instrumentator import Instrumentator
import redis
import json

redis_client = redis.Redis(host='localhost', port=6379, db=0)


app = FastAPI()
logger = setup_logger("query_service")

# Initialize Prometheus instrumentation
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5
    max_length: int = 50
    min_length: int = 20


def cache_response(query_key, response):
    """Cache response in Redis with an expiration time."""
    redis_client.set(query_key, json.dumps(response), ex=3600)  # Cache for 1 hour

def get_cached_response(query_key):
    """Retrieve cached response from Redis if available."""
    cached_response = redis_client.get(query_key)
    if cached_response:
        return json.loads(cached_response)
    return None

'''@app.post("/query/")
async def query_similar_records(request: QueryRequest):
    """Endpoint to retrieve similar records based on query text."""
    query_embedding = get_query_embedding(request.query)
    matched_ids = find_similar_embeddings(query_embedding, request.top_k)
    results = fetch_records(matched_ids)
    if not results:
        raise HTTPException(status_code=404, detail="No matching records found")
    return results'''

@app.post("/query/")
async def query_similar_records(request: QueryRequest):
    """Asynchronous endpoint to retrieve similar records."""
    query_embedding = await get_query_embedding(request.query)
    matched_ids = await find_similar_embeddings(query_embedding, request.top_k)
    results = await fetch_records(matched_ids)
    return results


'''@app.post("/rag/")
async def retrieve_and_generate_response(request: QueryRequest):
    """Retriever-Augmented Generation (RAG) endpoint for generating responses."""
    query_embedding = get_query_embedding(request.query)
    matched_ids = find_similar_embeddings(query_embedding, request.top_k)
    records = fetch_records(matched_ids)

    # Basic RAG: Create a custom response based on retrieved data
    response = f"Found {len(records)} related records for your query: {request.query}"
    for record in records:
        response += f"\n - User {record['user_id']} from {record['country']}: {record['user_review']}"
    return {"response": response}
'''

@app.post("/rag/")
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



def generate_personalized_rag_response(query, records, user_data):
    context = f"Query: {query}\nUser Location: {user_data['location']}\n\nSimilar records:\n" + "\n".join([f"- {rec['user_review']}" for rec in records])
    # Generate response using the model as in previous examples.
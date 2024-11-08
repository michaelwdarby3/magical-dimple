from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.query.retrieve_data import get_query_embedding, find_similar_embeddings, fetch_records
from src.query.rag_pipeline import generate_rag_response
from src.utils.log_utils import setup_logger
from prometheus_fastapi_instrumentator import Instrumentator


app = FastAPI()
logger = setup_logger("query_service")

# Initialize Prometheus instrumentation
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5
    max_length: int = 50
    min_length: int = 20


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
    request_info = {"query": request.query, "top_k": request.top_k}
    logger.info("Processing RAG request", extra=request_info)

    try:
        response = generate_rag_response(request.query, request.top_k, request.max_length, request.min_length)
        logger.info("RAG response generated successfully", extra={"response_length": len(response.get("response", ""))})
        return response
    except Exception as e:
        logger.error("Error in RAG pipeline", extra={"error": str(e), **request_info})
        raise HTTPException(status_code=500, detail="Error generating RAG response.")

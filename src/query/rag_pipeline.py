from transformers import pipeline, T5Tokenizer, T5ForConditionalGeneration
import torch
from src.query.retrieve_data import get_query_embedding, find_similar_embeddings, fetch_records
from src.utils.log_utils import setup_logger
from fastapi import HTTPException
import traceback
from prometheus_client import Counter, Histogram  # Add this line

# Initialize logging
logger = setup_logger("rag_pipeline")

# Load model and tokenizer for summarization
model_name = "t5-small"  # Use a suitable model for your task
model = T5ForConditionalGeneration.from_pretrained(model_name)
tokenizer = T5Tokenizer.from_pretrained(model_name)
qa_pipeline = pipeline("summarization", model=model, tokenizer=tokenizer)

# Prometheus metrics for RAG response generation
RAG_RECORDS_PROCESSED = Counter("rag_records_processed_total", "Total records processed in RAG pipeline")
RAG_PIPELINE_ERRORS = Counter("rag_pipeline_errors_total", "Total errors in RAG pipeline")

def generate_rag_response(query, top_k=5, product_name=None, product_type=None, max_length=100, min_length=5):
    """
    Generates a RAG response based on query and retrieved data using RAG.

    Parameters:
    - query (str): The input query from the user.
    - top_k (int): The number of similar records to retrieve.
    - product_name (str): Optional product name filter.
    - product_type (str): Optional product type filter.
    - max_length (int): Maximum length of the generated response.
    - min_length (int): Minimum length of the generated response.

    Returns:
    - dict: The generated RAG response and records used for the response.
    """
    try:
        logger.info(f"Generating RAG response for query: {query}")

        # Step 1: Get query embedding and find similar records
        query_embedding = get_query_embedding(query)
        matched_ids = find_similar_embeddings(query_embedding, top_k)

        # Step 2: Fetch filtered records based on optional product_name and product_type
        records = fetch_records(matched_ids, product_name=product_name, product_type=product_type)

        if not records:
            logger.warning("No records found for the query")
            return {"response": "No relevant information found.", "records": []}

        # Count the records processed for metrics
        RAG_RECORDS_PROCESSED.inc(len(records))

        context = f"Query: {query}\n\nRelated information:\n"
        for record in records:
            context += f"- User {record['user_id']} from {record['country']} reviewed '{record['product_name']}' ({record['product_type']}): {record['review_text']}\n"

        # Generate response using the language model
        inputs = tokenizer("summarize: " + context, return_tensors="pt")
        outputs = model.generate(inputs.input_ids, max_length=max_length, min_length=min_length, do_sample=True)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)

        logger.info("RAG response generated successfully")
        return {"response": response, "records": records}

    except Exception as e:
        RAG_PIPELINE_ERRORS.inc()  # Count pipeline errors
        error_message = f"Error generating RAG response: {e}"
        logger.error(error_message)
        logger.error(traceback.format_exc())
        return {"response": "", "error": error_message, "records": []}

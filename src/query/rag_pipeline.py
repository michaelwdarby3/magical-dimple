from transformers import pipeline, T5Tokenizer, T5ForConditionalGeneration
import torch
from src.query.retrieve_data import get_query_embedding, find_similar_embeddings, fetch_records
from src.utils.log_utils import setup_logger
from fastapi import HTTPException
import traceback

# Initialize logging
logger = setup_logger("rag_pipeline")

# Load model and tokenizer for summarization
model_name = "t5-small"  # Use a suitable model for your task
model = T5ForConditionalGeneration.from_pretrained(model_name)
tokenizer = T5Tokenizer.from_pretrained(model_name)
qa_pipeline = pipeline("summarization", model=model, tokenizer=tokenizer)


def generate_rag_response(query, top_k=5, max_length=100, min_length=5):
    """
    Generates a RAG response based on query and retrieved data using RAG.

    Parameters:
    - query (str): The input query from the user.
    - top_k (int): The number of similar records to retrieve.
    - max_length (int): Maximum length of the generated response.
    - min_length (int): Minimum length of the generated response.

    Returns:
    - dict: The generated RAG response.
    """
    try:
        logger.info(f"Generating RAG response for query: {query}")

        # Step 1: Get query embedding and find similar records
        query_embedding = get_query_embedding(query)
        matched_ids = find_similar_embeddings(query_embedding, top_k)

        # If no matches found
        if not matched_ids:
            logger.warning("No records found for the query")
            return {"response": "No relevant information found."}

        records = fetch_records(matched_ids)

        if not records:
            logger.warning("No records found for the query")
            return {"response": "No relevant information found."}

        # Step 2: Combine query and retrieved records for context
        context = f"Query: {query}\n\nRelated information:\n"
        for record in records:
            context += f"- User {record['user_id']} from {record['country']} said: {record['review_text']}\n"

        logger.info("Context for summarization generated successfully.")

        # Step 3: Generate response using the language model
        inputs = tokenizer("summarize: " + context, return_tensors="pt")
        outputs = model.generate(inputs.input_ids, max_length=max_length, min_length=min_length, do_sample=True)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        logger.info("RAG response generated successfully")

        return {"response": response}

    except Exception as e:
        error_message = f"Error generating RAG response: {e}"
        logger.error(error_message)
        logger.error(traceback.format_exc())  # Log the full traceback for debugging
        return {"response": "", "error": error_message}



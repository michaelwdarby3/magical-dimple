from transformers import pipeline
from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch
from src.query.retrieve_data import get_query_embedding, find_similar_embeddings, fetch_records
from src.utils.log_utils import setup_logger

# Initialize logging
logger = setup_logger("rag_pipeline")

# Load the summarization or question-answering pipeline from Hugging Face
model_name = "distilbert-base-uncased"  # You can experiment with other models like "gpt-2" or "distilbert"
qa_pipeline = pipeline("summarization", model=model_name)

'''# Load the fine-tuned model or experiment with other models like "gpt-2" or "t5-small"
model_name = "your-fine-tuned-model-path"
model = T5ForConditionalGeneration.from_pretrained(model_name)
tokenizer = T5Tokenizer.from_pretrained(model_name)
'''

def generate_rag_response(query, records, max_length=50, min_length=20):
    """Generate an enhanced RAG response based on query and similar records."""

    # Combine query and records into a single context
    context = f"Query: {query}\n\nSimilar records:\n" + "\n".join([f"- {rec['user_review']}" for rec in records])
    inputs = tokenizer("summarize: " + context, return_tensors="pt")

    # Generate response
    outputs = model.generate(inputs.input_ids, max_length=max_length, min_length=min_length, do_sample=True)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return {"response": response}



def generate_rag_response(query, top_k=5):
    """Generates a response based on query and retrieved data using RAG."""
    logger.info(f"Generating RAG response for query: {query}")

    # Step 1: Get query embedding and find similar records
    query_embedding = get_query_embedding(query)
    matched_ids = find_similar_embeddings(query_embedding, top_k)
    records = fetch_records(matched_ids)

    # Step 2: Combine query and retrieved records for context
    context = f"Query: {query}\n\nRelated information:\n"
    for record in records:
        context += f"- User {record['user_id']} from {record['country']} said: {record['user_review']}\n"

    # Step 3: Generate response using the language model
    response = qa_pipeline(context, max_length=100, min_length=25, do_sample=False)

    return {"response": response[0]["summary_text"]}

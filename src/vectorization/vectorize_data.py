import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from src.utils.log_utils import setup_logger
from concurrent.futures import ThreadPoolExecutor


# Initialize logging
logger = setup_logger("vectorization")

# Load the model
model = SentenceTransformer('all-MiniLM-L6-v2')


def load_text_data(data_path):
    """Load unstructured text data from JSON."""
    with open(data_path, 'r') as f:
        data = json.load(f)
    texts = [entry['user_review'] for entry in data]
    ids = [entry['user_id'] for entry in data]
    return texts, ids


'''def generate_embeddings(texts, batch_size=64):
    """Generate embeddings for a list of texts in batches."""
    logger.info("Generating embeddings in batches...")
    embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        batch_embeddings = model.encode(batch, show_progress_bar=True)
        embeddings.extend(batch_embeddings)
    return np.array(embeddings)'''

def generate_embeddings(texts, batch_size=64):
    """Generate embeddings for texts in parallel batches."""
    embeddings = []
    logger.info("Generating embeddings in batches...")
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(model.encode, texts[i:i+batch_size])
            for i in range(0, len(texts), batch_size)
        ]
        for future in futures:
            embeddings.extend(future.result())
    return np.array(embeddings)

def parallel_embedding_generation(texts, batch_size=64):
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(generate_embeddings, texts[i:i+batch_size])
            for i in range(0, len(texts), batch_size)
        ]
        embeddings = [future.result() for future in futures]
    return np.concatenate(embeddings)



def store_embeddings(embeddings, ids, index_path='vector_store.faiss'):
    """Store embeddings in FAISS index."""
    # Set up FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)

    # Add embeddings to the FAISS index
    logger.info("Storing embeddings in FAISS index...")
    index.add(embeddings)

    # Save index and mapping of IDs
    faiss.write_index(index, index_path)
    with open('id_map.json', 'w') as f:
        json.dump(ids, f)
    logger.info("Embeddings stored successfully.")


def vectorize_and_store(data_path):
    """Main function to load text data, vectorize, and store embeddings."""
    texts, ids = load_text_data(data_path)
    embeddings = generate_embeddings(texts)
    store_embeddings(embeddings, ids)
    logger.info("Vectorization and storage completed.")


if __name__ == "__main__":
    vectorize_and_store('data/preprocessed_data.json')

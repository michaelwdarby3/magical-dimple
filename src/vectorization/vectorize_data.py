import os
import json
import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from src.utils.log_utils import setup_logger
from concurrent.futures import ThreadPoolExecutor

# Initialize logging
logger = setup_logger("vectorization")

if os.getenv("BATCH_VECTORIZATION_ENABLED", "false").lower() != "true":
    print("Batch vectorization is disabled. Exiting vectorizer.")
    exit(0)

# Load the model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Data file paths
USER_DATA_PATH = 'data/users.csv'
REVIEW_DATA_PATH = 'data/reviews.csv'

def load_raw_data():
    """Load raw data from CSV files and merge relevant information."""
    users_df = pd.read_csv(USER_DATA_PATH)
    reviews_df = pd.read_csv(REVIEW_DATA_PATH)

    # Merge on user_id to associate reviews with user info
    merged_df = reviews_df.merge(users_df, on="user_id", how="left")

    return merged_df

def preprocess_data(df):
    """Clean and preprocess raw text data for vectorization."""
    df = df.dropna(subset=["review_text"])  # Remove reviews with missing text
    df["review_text"] = df["review_text"].str.lower()  # Convert text to lowercase
    df["review_text"] = df["review_text"].str.replace(r'\W+', ' ', regex=True)  # Remove non-alphanumeric characters

    # Return preprocessed text and corresponding IDs
    texts = df["review_text"].tolist()
    ids = df["review_id"].tolist()
    return texts, ids

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

def store_embeddings(embeddings, ids, index_path='vector_store.faiss'):
    """Store embeddings in FAISS index."""
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    logger.info("Storing embeddings in FAISS index...")
    index.add(embeddings)

    faiss.write_index(index, index_path)
    with open('id_map.json', 'w') as f:
        json.dump(ids, f)
    logger.info("Embeddings stored successfully.")

def vectorize_and_store():
    """End-to-end pipeline: Load, preprocess, vectorize, and store embeddings."""
    raw_data = load_raw_data()
    texts, ids = preprocess_data(raw_data)
    embeddings = generate_embeddings(texts)
    store_embeddings(embeddings, ids)
    logger.info("Vectorization and storage completed.")

if __name__ == "__main__":
    vectorize_and_store()

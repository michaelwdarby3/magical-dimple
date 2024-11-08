import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from src.utils.db_utils import get_db_connection

# Load pre-trained model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load FAISS index and ID mapping
index = faiss.read_index('src/vectorization/vector_store.faiss')
with open('src/vectorization/id_map.json', 'r') as f:
    id_map = json.load(f)

def get_query_embedding(query_text):
    """Generate embedding for the query text."""
    return np.array([model.encode(query_text)])

def find_similar_embeddings(query_embedding, k=5):
    """Find top-k similar embeddings using FAISS."""
    _, indices = index.search(query_embedding, k)
    # Retrieve matching user IDs from ID map
    matched_ids = [id_map[idx] for idx in indices[0]]
    return matched_ids

def fetch_records(matched_ids):
    """Fetch records from the database based on matched IDs."""
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE user_id = ANY(%s)", (matched_ids,))
        results = cursor.fetchall()
    connection.close()
    return results

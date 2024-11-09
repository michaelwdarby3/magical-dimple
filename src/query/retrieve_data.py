import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from src.utils.db_utils import get_db_connection
import os

# Load pre-trained model
model = SentenceTransformer('all-MiniLM-L6-v2')

INDEX_PATH = 'src/vectorization/vector_store.faiss'
ID_MAP_PATH = 'src/vectorization/id_map.json'


def fetch_documents():
    """
    Fetches text documents from the database (e.g., review texts from the reviews table).

    Returns:
    - list of str: A list of document texts.
    """
    connection = get_db_connection()  # Establish database connection
    query = "SELECT review_text FROM reviews;"  # Query to fetch all review texts
    with connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
    connection.close()

    # Extract the text content from the query results
    return [row[0] for row in results]


'''def generate_and_store_embeddings(documents, index_path=INDEX_PATH):
    """
    Generates embeddings for the provided documents, creates a FAISS index, and saves it.

    Parameters:
    - documents (list of str): List of text documents to vectorize.
    - index_path (str): Path to store the FAISS index file.
    """
    # Generate embeddings
    embeddings = model.encode(documents)

    # Create FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)  # Using L2 distance (change based on needs)
    index.add(embeddings)  # Add embeddings to the FAISS index

    # Save the index
    faiss.write_index(index, index_path)
    print(f"FAISS index saved at {index_path}")'''


def generate_and_store_embeddings(documents, index_path=INDEX_PATH, id_map_path=ID_MAP_PATH):
    """
    Generates embeddings for the provided documents, creates a FAISS index, and saves it along with an ID map.

    Parameters:
    - documents (list of tuple): List of tuples (review_id, review_text).
    - index_path (str): Path to store the FAISS index file.
    - id_map_path (str): Path to store the ID mapping file.
    """
    # Separate IDs and document texts
    ids, texts = zip(*documents)

    # Generate embeddings
    embeddings = model.encode(texts)

    # Create FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)  # Using L2 distance (change based on needs)
    index.add(embeddings)  # Add embeddings to the FAISS index

    # Save the index
    faiss.write_index(index, index_path)
    print(f"FAISS index saved at {index_path}")

    # Create and save ID map
    id_map = {i: str(ids[i]) for i in range(len(ids))}  # Map FAISS indices to document IDs
    with open(id_map_path, 'w') as f:
        json.dump(id_map, f)
    print(f"ID map saved at {id_map_path}")


# Check if FAISS index exists; if not, fetch data, generate it, and save
if not os.path.exists(INDEX_PATH):
    print("FAISS index not found. Generating a new one...")
    documents = fetch_documents()  # Fetch actual documents from the database
    generate_and_store_embeddings(documents)
else:
    print("FAISS index loaded from disk.")
    index = faiss.read_index(INDEX_PATH)


# Load FAISS index and ID mapping
index = faiss.read_index(INDEX_PATH)
with open(ID_MAP_PATH, 'r') as f:
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

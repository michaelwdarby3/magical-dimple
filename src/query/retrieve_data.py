import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from src.utils.db_utils import get_db_connection
import os
import psycopg2.extras

# Load pre-trained model
model = SentenceTransformer('all-MiniLM-L6-v2')

INDEX_PATH = 'src/vectorization/vector_store.faiss'
ID_MAP_PATH = 'src/vectorization/id_map.json'

# Initialize index and id_map as global variables
index = None
id_map = None



def fetch_documents(product_name=None, product_type=None):
    """
    Fetches text documents from the database, optionally filtering by product_name or product_type.

    Parameters:
    - product_name (str, optional): The specific product name to filter by.
    - product_type (str, optional): The specific product type to filter by.

    Returns:
    - list of tuple: A list of tuples containing (review_id, review_text).
    """
    connection = get_db_connection()  # Establish database connection
    query = "SELECT review_id, review_text FROM reviews WHERE 1=1"
    params = []

    if product_name:
        query += " AND product_name = %s"
        params.append(product_name)
    if product_type:
        query += " AND product_type = %s"
        params.append(product_type)

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        results = cursor.fetchall()
    connection.close()

    return results


def generate_and_store_embeddings(documents, index_path=INDEX_PATH, id_map_path=ID_MAP_PATH):
    """
    Generates embeddings for the provided documents, creates a FAISS index, and saves it along with an ID map.

    Parameters:
    - documents (list of tuple): List of tuples (review_id, review_text).
    - index_path (str): Path to store the FAISS index file.
    - id_map_path (str): Path to store the ID mapping file.
    """
    global index, id_map
    ids, texts = zip(*documents)

    # Generate embeddings
    embeddings = model.encode(texts)

    # Create FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    faiss.write_index(index, index_path)
    print(f"FAISS index saved at {index_path}")

    # Create and save ID map
    id_map = {str(i): str(ids[i]) for i in range(len(ids))}  # Ensure keys are strings for consistent access
    with open(id_map_path, 'w') as f:
        json.dump(id_map, f)
    print(f"ID map saved at {id_map_path} with {len(id_map)} entries.")

def load_index_and_id_map(force_rebuild=False):
    """Load FAISS index and ID map if they are not already loaded, or force a rebuild."""
    global index, id_map

    if force_rebuild or not os.path.exists(INDEX_PATH) or not os.path.exists(ID_MAP_PATH):
        print("Forcing regeneration of FAISS index and ID map...")
        documents = fetch_documents()
        generate_and_store_embeddings(documents)
    else:
        # Load existing index and ID map
        index = faiss.read_index(INDEX_PATH)
        print("Loaded FAISS index from disk.")
        with open(ID_MAP_PATH, 'r') as f:
            id_map = json.load(f)
        print("Loaded ID map from disk.")

# Force reload the index and ID map on startup
load_index_and_id_map(force_rebuild=True)

def get_query_embedding(query_text):
    """Generate embedding for the query text."""
    embedding = np.array([model.encode(query_text)])
    print(f"Generated query embedding of shape: {embedding.shape}")
    return embedding

def find_similar_embeddings(query_embedding, k=5):
    """Find top-k similar embeddings using FAISS."""
    global index, id_map
    load_index_and_id_map()  # Ensure index and id_map are loaded

    D, indices = index.search(query_embedding, k)
    print(f"Indices found: {indices}, Distances: {D}")

    matched_ids = [id_map.get(str(idx), None) for idx in indices[0] if str(idx) in id_map]
    matched_ids = [id for id in matched_ids if id is not None]

    if not matched_ids:
        print("No matches found in the ID map for the query.")
    else:
        print(f"Matched IDs: {matched_ids}")

    return matched_ids

def fetch_records(matched_ids, product_name=None, product_type=None):
    """
    Fetch records from the database based on matched IDs, optionally filtering by product_name and/or product_type.

    Parameters:
    - matched_ids (list of str): List of review IDs to retrieve.
    - product_name (str, optional): The specific product name to filter by.
    - product_type (str, optional): The specific product type to filter by.

    Returns:
    - list of dict: A list of records with fields user_id, country, review_text, product_name, product_type.
    """
    connection = get_db_connection()
    base_query = "SELECT * FROM reviews WHERE review_id = ANY(%s)"
    params = [matched_ids]

    # Adjust query based on optional product_name and product_type filters
    if product_name and product_type:
        base_query += " AND product_name = %s AND product_type = %s"
        params.extend([product_name, product_type])
    elif product_name:
        base_query += " AND product_name = %s"
        params.append(product_name)
    elif product_type:
        base_query += " AND product_type = %s"
        params.append(product_type)

    with connection.cursor() as cursor:
        cursor.execute(base_query, params)
        results = cursor.fetchall()

    # Map results to a list of dictionaries for easier use
    records = [
        {
            "user_id": row[1],  # Assuming user_id is in the 2nd column
            "country": row[2],  # Adjust indices as per actual table structure
            "review_text": row[3],
            "product_name": row[4],
            "product_type": row[5],
        }
        for row in results
    ]
    connection.close()

    return records




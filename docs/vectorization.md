
# Vectorization Documentation

The vectorization process in this project transforms unstructured text data into embeddings, which are dense vector representations. These embeddings are stored in a FAISS (Facebook AI Similarity Search) vector database, enabling efficient retrieval of similar records based on user queries.

This document provides an overview of the vectorization process, how to use the vectorization module, and the configuration of FAISS for optimized querying.

---

## Overview of Vectorization Process

### Purpose
The purpose of vectorization is to enable quick and accurate retrieval of records by converting text data into numerical vectors. These vectors capture the semantic meaning of text, allowing us to find records that are "similar" in meaning rather than relying on exact keyword matches. This approach is particularly useful for the **Retriever-Augmented Generation (RAG)** setup, as it enhances query-response relevance.

### Model Used
This project utilizes the `all-MiniLM-L6-v2` model from `sentence-transformers`, which is well-suited for efficient and meaningful text embeddings. 

---

## Key Components of the Vectorization Pipeline

### 1. Data Loading
Text data is loaded from a JSON file (default: `data/preprocessed_data.json`) which includes:
- `user_review`: the main text content for vectorization
- `user_id`: a unique identifier for each review or record

These are passed to the vectorization function to generate embeddings.

### 2. Embedding Generation
The vectorization script uses a **batching** strategy to handle larger datasets efficiently. Here are the main steps:
- The data is divided into batches (default: 64 records per batch).
- Each batch is processed in parallel using `ThreadPoolExecutor` to enhance speed.
- The embeddings are generated for each batch and aggregated to form the complete embedding dataset.

### 3. FAISS Index Creation
FAISS is utilized for storing and querying the generated embeddings:
- **Index Type**: We use `IndexFlatL2`, which calculates L2 distance (Euclidean) between vectors for similarity matching.
- The embeddings are stored in FAISS, and an ID map (`id_map.json`) links each embedding to its corresponding review `user_id`.

This approach makes it easy to retrieve the original records after querying based on the vector similarity.

---

## Configuring and Running the Vectorization Process

The vectorization process can be run as an optional, **batch vectorization step** within the overall pipeline. Here’s how it’s set up:

### Command Line Execution
The vectorization script (`vectorize_data.py`) can be run independently to generate the vector database:
```bash
docker-compose run vectorizer
```
This command will:
1. Load the data from `data/preprocessed_data.json`.
2. Generate embeddings and store them in FAISS.
3. Output `vector_store.faiss` and `id_map.json` files.

### Script Walkthrough: `vectorize_data.py`

#### Key Functions
1. **`load_text_data(data_path)`**  
   Loads the JSON file specified in `data_path` and extracts the `user_review` text data and `user_id` identifiers.
   
2. **`generate_embeddings(texts, batch_size)`**  
   Uses the `sentence-transformers` model to create embeddings in batches, leveraging parallel processing for efficiency.
   
3. **`store_embeddings(embeddings, ids, index_path)`**  
   Stores the embeddings in a FAISS index file and saves the ID map linking each vector to its `user_id`.

4. **`vectorize_and_store(data_path)`**  
   Combines the above functions to load data, generate embeddings, and store them, enabling easy execution.

### Example Usage
After modifying `docker-compose.yml` to include a conditional vectorizer service, use the following command:
```bash
docker-compose up vectorizer
```
This will batch-process the vectorization data and exit upon completion.

---

## FAISS and Vector Database Storage

### Index Details
The FAISS vector index (`vector_store.faiss`) and ID map (`id_map.json`) are the outputs of the vectorization step:
- **Index Path**: `src/vectorization/vector_store.faiss`
- **ID Map Path**: `src/vectorization/id_map.json`

These files are required for efficient retrieval in the RAG pipeline. The `vector_store.faiss` file holds the numerical embeddings, while the `id_map.json` file links each embedding back to the original text data for retrieval.

---

## Using Vectorization in RAG Queries

Once the embeddings are generated and stored, they can be queried within the **Retriever-Augmented Generation** pipeline. The RAG pipeline will:
1. Convert a user’s query into a vector.
2. Use FAISS to retrieve the most similar vectors.
3. Map the retrieved vectors to original records using `id_map.json`.

### Sample Workflow
1. **Query Input**: A user inputs a text query.
2. **Vector Matching**: The query is converted into a vector and matched against `vector_store.faiss` using FAISS.
3. **ID Retrieval**: The IDs of the closest matches are fetched from `id_map.json`.
4. **Record Fetching**: The matching records are retrieved from the database and used to generate a relevant response.

---

## Summary and Best Practices

- **Batch Vectorization**: It’s recommended to run vectorization as a batch process before handling queries to ensure the FAISS index is fully populated.
- **File Management**: Ensure `vector_store.faiss` and `id_map.json` are present and up-to-date before starting the API server.
- **Parallel Processing**: The vectorization script is optimized for batch processing with parallel embedding generation. Ensure sufficient resources are allocated when running large batches.

---

This document should guide you through understanding and using the vectorization process within this project. The configuration enables efficient and scalable data retrieval, making it easier to handle large volumes of unstructured text.

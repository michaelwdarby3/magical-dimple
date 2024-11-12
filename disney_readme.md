# Project Overview: LLM Data Engineering Pre-Assignment
This document summarizes how each assignment requirement has been addressed, detailing specific project components and workflows used to fulfill each objective.

---

## 1. Data Ingestion
### Requirement
Provide a dataset (e.g., JSON, CSV, or unstructured text files) that includes a mix of structured and unstructured data. Create a pipeline to load this data into a database of choice, optimizing schema for querying.

### Implementation
- Data Files: The dataset includes users.csv and reviews.csv to represent structured and semi-structured data. Each record includes user demographics, textual reviews, and product details. I generated these myself.
- Schema Design:
  - The schema optimizes data retrieval by using UUIDs as primary keys for efficient indexing and relationships between users and reviews.
  - Columns such as review_text, product_name, and product_type capture unstructured and semi-structured data.
- Database Ingestion Pipeline:
  - The init.sql script initializes the database schema, loading data directly into PostgreSQL tables upon container startup.
  - CSV files are mounted for ingestion to ensure reproducibility and easy updates.
  - The vectorizer service can batch-process embeddings to initialize the vector store efficiently.

--- 

## 2. Data Preprocessing
### Requirement
Handle noise, transform data (e.g., clean text, handle missing values), and preprocess data for efficient storage and retrieval.

### Implementation
- Preprocessing Step:
  - The preprocess_data.py script handles initial text cleaning, such as removing extra whitespace and special characters.
  - Data transformations include normalization and field structuring (e.g., converting timestamps).
  - This processed data is stored in preprocessed_data.json for streamlined ingestion and vectorization.
- Optional Batch Processing:
  - Batch vectorization via the vectorizer service allows bulk embedding generation for the RAG pipeline, optimizing retrieval performance and avoiding redundant computations.

--- 
## 3. Vectorization
### Requirement
Use a pre-trained language model or embeddings model to convert unstructured text into embeddings. Store embeddings in a vector store with batch processing for larger datasets.

### Implementation
- Embeddings Model:
  - SentenceTransformer with all-MiniLM-L6-v2 is used to generate embeddings for review_text, capturing semantic information.
- Vector Storage Solution:
  - FAISS is employed for efficient vector indexing and retrieval.
  - Batch Processing: The vectorize_data.py script supports batch processing and concurrent embedding generation to improve scalability.
  - Embeddings are stored persistently in a FAISS index, facilitating efficient similarity search.

---

## 4. Query and Retrieve
### Requirement
Create an API or script to allow querying based on text prompts. Retrieve similar embeddings and return corresponding records from the database. Implement Retriever-Augmented Generation (RAG) for summary generation.

### Implementation
- API Setup:
  - A FastAPI-based API exposes endpoints for querying, retrieval, and RAG operations.
  - Endpoints:
    - /query/rag: Retrieves relevant records using FAISS, then uses a language model to generate summaries or responses based on query context.
- RAG Pipeline:
  - The RAG pipeline (rag_pipeline.py) combines embedding retrieval with the T5-based language model for generating contextual summaries.
  - The query_service.py fetches data from both the vector store and database, supporting various filters (e.g., by product_name or product_type) to refine retrieval.

---

## 5. Documentation
### Requirement
Document code, design choices, and any trade-offs (e.g., schema design, vector storage approach).

### Implementation
- Detailed Documentation:
  - Each component has an associated .md file, covering usage, setup, design choices, and configuration.
  - Specific documentation files include:
    - vectorization.md: Details embedding generation and vector storage.
    - data_ingestion.md: Explains ingestion, schema design, and table structure.
    - rag_pipeline.md: Provides an overview of the retrieval and generation steps.
    - prometheus.md and grafana.md: Outline monitoring, metrics, and dashboard usage.
  - README: Serves as an entry point with system setup, usage examples, and service descriptions.
- Design Choices & Trade-offs:
  - Schema design optimizations focus on query performance and retrieval speed.
  - Vectorization with FAISS was chosen for its scalability and efficiency, balanced against memory usage.

---

## 6. Bonus
### Requirement
Implement monitoring/logging for the data pipeline. Optimize for scalability (e.g., larger files or parallel processing).

### Implementation
- Monitoring & Metrics:
  - Prometheus gathers system and application metrics (e.g., response times, database status).
  - Grafana visualizes metrics, with pre-configured dashboards tailored for FastAPI performance, database health, and vectorization insights.
- Scalability Optimizations:
  - Batch Processing: Supports large datasets through parallel embedding generation in vectorize_data.py.
  - Concurrent Processing: The use of ThreadPoolExecutor in vectorization enables scalable, efficient data processing.
  - Replicas: The use of docker-compose and nginx to create multiple instances of the app shows that it is easily scaled depending on your needs.
  - Load balancing: Requests are distributed evenly between all instances of the app.

---

## Testing

Prerequisite: To test this app, you should have Docker and docker-compose installed locally. 
### Steps
1. From within a terminal, navigate to the root of this project.
2. Use docker-compose to build and spin up the project. 
   1. To test without batch vectorization enabled: Run `docker-compose up -d --build`
   2. To test with batch vectorization enabled: Run `BATCH_VECTORIZATION_ENABLED=true docker-compose up -d --build`
3. Wait for the project to install, build, and spin up. This may take some time, I would estimate 5-20 minutes depending on your machine.
4. Once Docker logs are indicating that the health checks for magical-dimple-app-1, -2, and -3 are up (or when you've waited long enough), navigate to http://localhost:8501/ to check out the FastAPI and streamlit dashboard (the main rag interface).
5. Run queries on the data; I'd recommend first testing with simple queries like "good", "product", or "time".
6. Test out product_name and product_type. These fields are finicky because the dataset is relatively small.
7. You can also run curl commands, such as the following, to test the app:
   ``` bash
   curl -X POST "http://localhost:8000/query/rag" -H "Content-Type: application/json" -d '{
    "query": "good",
    "top_k": 5,
    "product_name": "Dyson V11 Vacuum"
     }' 
    ```
7. Navigate to http://localhost:9090/ to check out prometheus. Add in metrics queries to see how your usage is tracked.
8. Navigate to http://localhost:3000/ to check out grafana. Login with the provided credentials "admin" and "default123".
9. Click into "Dashboards", then "FastAPI Service Dashboard", to view some of the metrics used from Prometheus.
10. For further API description, view http://localhost:8000/docs.

## Conclusion
This project meets all specified requirements, including ingestion, preprocessing, vectorization, querying, and Retriever-Augmented Generation, with comprehensive monitoring and scalability features. Each component is well-documented, and the pipeline can handle high-demand data retrieval and response generation efficiently.
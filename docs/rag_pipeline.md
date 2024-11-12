# Retriever-Augmented Generation (RAG) Pipeline
This document provides a detailed guide on the RAG pipeline, including its configuration, components, usage, and setup instructions.

--- 

## Overview
The Retriever-Augmented Generation (RAG) pipeline enhances response quality by combining retrieval and generation. This hybrid approach grounds the generated response in actual data, which enhances accuracy and relevance.

--- 

## Workflow
- Retrieve: Given a query, the pipeline searches a vector store for the most relevant document embeddings.
- Generate: Retrieved documents serve as context for the language model, which generates a response based on this information.

--- 

## Configuration
### Models in Use
- Retriever Model: A pre-trained model (e.g., all-MiniLM-L6-v2 from sentence-transformers) creates embeddings for stored documents and queries.
- Generator Model: The T5 model (t5-small), used to generate responses based on retrieved context, is both efficient and well-suited for summarization.
Vector Storage

The pipeline uses FAISS for vector storage, which stores and retrieves embeddings efficiently. Ensure that faiss is installed and properly configured. Additionally, stored embeddings are managed through an ID map file, facilitating the alignment of stored vectors with their respective documents.

--- 

## Setting Up the RAG Pipeline
The RAG pipeline configuration is primarily managed in rag_pipeline.py, with supporting files as follows:

- Vectorization: Use vectorize_data.py in the vectorization/ directory to batch-generate and store embeddings from document data, ensuring that vector data is up-to-date.
- Model Loading: Use model_utils.py to handle retriever and generator model loading and configuration.
Key Components and Parameters
- Retrieval Parameters: top_k specifies the number of similar documents to retrieve, directly influencing response diversity.
- Filtering Options: Filtering by product_name and product_type is supported, enabling more targeted retrieval based on these document attributes.
- Response Control: Adjust parameters such as max_length and min_length to control the length and format of generated responses.

--- 

## Usage Instructions
To query the RAG pipeline, use the /query/rag API endpoint. Below is an example of a query request:

```json
POST /query/rag
{
  "query": "How is the battery life of this product?",
  "top_k": 5,
  "product_name": "Wireless Earbuds",
  "product_type": "Electronics"
}
```

## Response Format
The RAG endpoint responds with a generated summary and the records used to construct it, providing both contextual and generated insights. Example response:

```json
Copy code
{
  "response": "The battery life of the Wireless Earbuds is excellent, with users reporting long usage times between charges.",
  "records": [
    {
      "user_id": "abc123",
      "country": "USA",
      "review_text": "Great battery life on these earbuds...",
      "product_name": "Wireless Earbuds",
      "product_type": "Electronics"
    },
    ...
  ]
}
```
--- 


## Troubleshooting and Optimization Tips
- Empty or Unexpected Responses: Ensure that document embeddings are accurately generated and that filters such as product_name and product_type match your data.
- Slow Retrieval Times: Consider batch-processing embeddings, and optimize FAISS configurations for faster indexing.
Additional References
- Endpoints: Refer to api_reference.md for additional details on the RAG pipeline endpoints and parameters.
- Batch Vectorization: If using batch-processing, see vectorization.md for more on efficient embedding storage.

# Retriever-Augmented Generation (RAG) Pipeline

This document provides an overview of the RAG pipeline, detailing its components, configuration, and usage.

## Overview

The Retriever-Augmented Generation (RAG) pipeline combines a retrieval system with a language model to generate responses based on relevant context. This setup improves response accuracy by grounding generation in actual data.

## Workflow

1. **Retrieve**: Given a query, the pipeline searches a vector store for relevant document embeddings.
2. **Generate**: The retrieved documents are fed into a language model, which generates a response based on the context.

## Configuration

### Model Configuration

- **Retriever Model**: This model generates embeddings for documents and queries. It typically uses a pre-trained transformer model like `distilbert` or `roberta`.
- **Generator Model**: A pre-trained language model, such as `GPT-2` or `BART`, is used for generating responses.

### Embedding Vector Storage

The RAG pipeline relies on vector storage (like `faiss`) to store and retrieve embeddings. Ensure `faiss` is installed and configured.

## Setting Up the RAG Pipeline

The RAG pipeline is configured and run via `rag_pipeline.py`. Ensure the following steps:

1. **Load Models**: Use `model_utils.py` to load both retriever and generator models.
2. **Vectorize Data**: Use `vectorize_data.py` in `vectorization/` to generate and store embeddings for document data.

### Example

To query the RAG pipeline, use the `/query/rag` endpoint in the API:

```json
POST /query/rag
{
  "query": "What is the quality of service?",
  "top_k": 5
}
```

## Troubleshooting

- **Empty Response**: Ensure embeddings are loaded and retriever is correctly configured.
- **Slow Response Time**: Use batch processing in `faiss` and optimize vector storage.

Refer to `api_reference.md` for detailed endpoint documentation.

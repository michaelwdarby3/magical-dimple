
# API Reference

This document provides a detailed reference for each API endpoint available in the Retriever-Augmented Generation (RAG) system.

## Base URL

All endpoints are prefixed with the base URL, which is typically:
```plaintext
http://localhost:8000
```

## Endpoints

### 1. `/query/rag`

- **Method**: POST
- **Description**: Retrieves a response from the Retriever-Augmented Generation pipeline based on a query.

#### Request Body

The request accepts the following JSON fields:

```json
{
  "query": "Text of the user query",
  "top_k": 5,
  "product_name": "Example Product",
  "product_type": "Product Type",
  "max_length": 100,
  "min_length": 5
}
```

- **query** (string): Main text query for the RAG system.
- **top_k** (integer, optional): Number of similar records to retrieve. Default is 5.
- **product_name** (string, optional): Product name filter.
- **product_type** (string, optional): Product type filter.
- **max_length** (integer, optional): Maximum length of generated response.
- **min_length** (integer, optional): Minimum length of generated response.

#### Example Request

```bash
curl -X POST "http://localhost:8000/query/rag" -H "Content-Type: application/json" -d '{
    "query": "Customer service feedback",
    "top_k": 3,
    "product_name": "Vacuum Cleaner",
    "product_type": "Appliance",
    "max_length": 80,
    "min_length": 10
}'
```

#### Example Response

```json
{
  "response": "The customer feedback for Vacuum Cleaner is overwhelmingly positive...",
  "records": [
    {
      "user_id": "12345",
      "country": "USA",
      "review_text": "Very satisfied with the performance of the vacuum.",
      "product_name": "Vacuum Cleaner",
      "product_type": "Appliance"
    },
    {
      "user_id": "67890",
      "country": "Canada",
      "review_text": "Effective suction and easy to use.",
      "product_name": "Vacuum Cleaner",
      "product_type": "Appliance"
    }
  ]
}
```

### 2. `/health`

- **Method**: GET
- **Description**: Health check endpoint to verify if the service is running.
- **Response**:

```json
{
  "status": "ok"
}
```

### 3. `/metrics`

- **Method**: GET
- **Description**: Exposes Prometheus-compatible metrics for system monitoring.

Access this endpoint via **[Prometheus at http://localhost:9090](http://localhost:9090)** for monitoring.

## Notes

- All endpoints are accessible at their default URLs as specified.
- The RAG response endpoint provides flexibility in retrieving records by allowing filters such as `product_name` and `product_type`, which can be adjusted based on query requirements.

For further details on service usage, refer to the **dashboard_guide.md** in the documentation.


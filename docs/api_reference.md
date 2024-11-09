
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
- **Description**: Retrieves a response based on the Retriever-Augmented Generation pipeline.
- **Request Body**:

    ```json
    {
      "query": "What is the quality of service?",
      "top_k": 5
    }
    ```

- **Response**:

    ```json
    {
      "response": "The service quality is excellent, highly recommended."
    }
    ```

- **Use Case**: Use this endpoint to generate responses grounded in context data.

---

### 2. `/data/users`

- **Method**: GET
- **Description**: Retrieves user information.
- **Response**:

    ```json
    [
      {
        "user_id": "123e4567-e89b-12d3-a456-426614174000",
        "name": "Alice",
        "age": 30,
        "country": "USA"
      }
    ]
    ```

- **Use Case**: Fetches a list of users in the system.

---

### 3. `/data/reviews`

- **Method**: GET
- **Description**: Retrieves review data.
- **Response**:

    ```json
    [
      {
        "review_id": "789e4567-e89b-12d3-a456-426614174111",
        "user_id": "123e4567-e89b-12d3-a456-426614174000",
        "review_text": "Excellent product quality.",
        "created_at": "2024-01-01T12:00:00"
      }
    ]
    ```

- **Use Case**: Retrieves reviews submitted by users.

---

### 4. `/feedback`

- **Method**: POST
- **Description**: Submit feedback for a generated response.
- **Request Body**:

    ```json
    {
      "query": "What is the quality of service?",
      "response": "Excellent",
      "rating": 5
    }
    ```

- **Response**:

    ```json
    {
      "status": "Feedback submitted successfully."
    }
    ```

- **Use Case**: Allows users to submit feedback on generated responses.

---

### 5. `/feedback/summary`

- **Method**: GET
- **Description**: Retrieves a summary of feedback ratings.
- **Response**:

    ```json
    [
      {
        "query": "What is the quality of service?",
        "average_rating": 4.7,
        "response_count": 15
      }
    ]
    ```

- **Use Case**: Provides insights into feedback on generated responses.

---

## Error Codes

- **400**: Bad Request – Invalid or missing parameters in the request body.
- **404**: Not Found – The requested resource does not exist.
- **500**: Internal Server Error – An error occurred on the server.

Refer to this document when working with API endpoints to understand expected inputs and outputs.

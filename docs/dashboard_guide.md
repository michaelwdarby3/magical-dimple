
# Dashboard Guide

This document provides an overview of the Streamlit dashboard, including instructions for accessing and using its features.

## Overview

The Streamlit dashboard allows users to interact with the Retriever-Augmented Generation (RAG) system, query responses, and view feedback summaries.

## Accessing the Dashboard

To access the dashboard, navigate to:
```plaintext
http://localhost:8501
```
Ensure the `app` and `dashboard` services are running in Docker if using a Dockerized setup.

## Dashboard Features

### Query RAG Response

1. **Input Query**: Enter a query in the text input field to retrieve a response.
2. **Top-K Results**: Use the slider to adjust the number of results (Top-K) that the retriever model should fetch.
3. **Submit**: Click the "Submit Query" button to get the RAG-generated response.

The response will be displayed below, providing contextual answers based on the data.

### Feedback Summary

The feedback section displays a summary of feedback on generated responses.

- **Ratings Table**: Shows the average rating for each query and the count of responses rated.
- **View Feedback**: Provides insights into which queries have the best or worst ratings.

## Screenshots

![Dashboard Overview](path/to/dashboard-overview.png)

## Troubleshooting

- **No Response for Query**: Ensure the RAG pipeline is configured correctly and data is loaded.
- **Dashboard Not Loading**: Verify that the `dashboard` service is running and accessible on port 8501.

Refer to the API documentation (`api_reference.md`) for more details on endpoints used in the dashboard.


# Streamlit Dashboard

## Overview
The Streamlit dashboard provides an interactive interface for querying and analyzing data within the project. This dashboard enables users to submit queries, specify parameters, and view generated responses and related records. It's a central hub that connects users with the project's FastAPI backend, allowing for Retriever-Augmented Generation (RAG) queries, and is integrated with Prometheus and Grafana for monitoring.

## Getting Started

### Accessing the Dashboard
- URL: [http://localhost:8501](http://localhost:8501)

Ensure that all services are running (including `app`, `db`, `nginx`, `prometheus`, and `grafana`). The dashboard depends on the FastAPI app backend to retrieve and display results.

### Key Components
- **Query Input**: Submit a text prompt to retrieve relevant records and generate responses.
- **Top-K Slider**: Adjust the number of similar records to retrieve based on the query input.
- **Product Name & Product Type Filters**: Optional fields to filter queries by product characteristics.
- **Country Filter**: Optional field to filter results based on the user’s country.

## Usage

1. **Enter a Query**: In the sidebar, type your query prompt in the "Enter a search query" field.
2. **Adjust Parameters** (optional):
   - Use the sliders and text input fields to refine the query based on `top_k`, product details, or country.
3. **Retrieve Similar Records**: Click the **"Retrieve Similar Records"** button to run the query.
4. **View Results**:
   - The dashboard displays a generated response along with any retrieved records matching the query.

## Features

- **Dynamic RAG Generation**: The dashboard provides responses using the Retriever-Augmented Generation (RAG) model.
- **Integrated Monitoring**: The dashboard tracks query submissions, response times, and error logs via Prometheus.
- **User Feedback**: Users can rate the response for further evaluation.

## Integration with Monitoring Services

### Prometheus Metrics
Prometheus tracks the following metrics for Streamlit:
- **Query Counts**: Number of queries submitted.
- **Response Times**: Average response time per query.
- **Error Tracking**: Logs unsuccessful query attempts for debugging.

To view Prometheus metrics, navigate to: [http://localhost:9090](http://localhost:9090).

### Grafana Dashboards
Grafana provides a visual dashboard to analyze metrics from Prometheus. It includes real-time graphs for query frequency, response times, and application health.

Access Grafana at: [http://localhost:3000](http://localhost:3000)

## Troubleshooting

- **Data Not Loading**: Verify all services are active, especially `app` and `db`.
- **Metrics Not Visible**: Ensure Prometheus and Grafana are running and properly configured.
- **Unresponsive Interface**: Restart the Streamlit service.

Refer to the main README.md for further setup and troubleshooting instructions.

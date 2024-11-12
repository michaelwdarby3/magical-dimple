
# Project Title: Retriever-Augmented Generation System for Reviews and Recommendations

![Project Banner](assets/banner.png)

## Overview

This project implements a **Retriever-Augmented Generation (RAG) system** to handle reviews and recommendations. It ingests data into a PostgreSQL database, uses FAISS for embedding retrieval, and exposes an API through FastAPI for querying. Users can access insights via a **Streamlit dashboard**, monitor performance with **Prometheus**, and view visualizations in **Grafana**.

## Key Components

- **FastAPI**: Provides API endpoints for retrieving review records and generating responses based on queries.
- **PostgreSQL**: Stores structured review data in an optimized schema.
- **FAISS**: Manages vectorized embeddings for efficient similarity search.
- **Streamlit**: Frontend dashboard for querying and interacting with data.
- **Prometheus**: Collects and monitors metrics, with custom configuration for the RAG pipeline.
- **Grafana**: Visualizes metrics data with pre-configured dashboards.

## Getting Started

### Prerequisites

- **Docker** and **Docker Compose** installed on your machine.

### Setup and Run

1. **Clone the repository**: Download or clone this project repository.
2. **Build and start services**:

   ```bash
   docker-compose up -d --build
   ```

3. **Access Services**:

   - **API (FastAPI)**: [http://localhost:8000](http://localhost:8000)
   - **Streamlit Dashboard**: [http://localhost:8501](http://localhost:8501)
   - **Prometheus**: [http://localhost:9090](http://localhost:9090)
   - **Grafana**: [http://localhost:3000](http://localhost:3000)

4. **Grafana Access**: Login with the default Grafana credentials:
   - Username: `admin`
   - Password: `default123`

## Using the Dashboards

### Streamlit Dashboard

The Streamlit dashboard provides a user-friendly interface to query the review data based on keywords or specific product information.

1. **Enter Query**: In the left sidebar, input a search query to retrieve similar records.
2. **Select Filters**:
   - `Product Name` and `Product Type`: Optional fields to refine search.
3. **View Results**: Results are displayed with user and review information, and you can rate the retrieved response.

### Prometheus Metrics

Prometheus collects real-time metrics and provides a foundation for monitoring and alerting.

- Access the Prometheus dashboard and search for metrics like `http_requests_total`, `rag_records_processed_total`, etc.
- Metrics are organized to track RAG operations, API performance, and system health.

### Grafana Dashboards

Grafana offers visualized metrics from Prometheus data.

1. **Access the pre-configured dashboard** in Grafana for RAG pipeline metrics.
2. **View Metrics**:
   - Track the rate of requests, response times, and processed records.
   - Identify potential bottlenecks in the vectorization and retrieval processes.

## System Design Overview

### Data Ingestion

The system loads structured review data into PostgreSQL. Data ingestion is automated, ensuring a consistent data schema for querying.

### Preprocessing and Vectorization

- **Preprocessing**: Ensures text data is clean and optimized for vectorization.
- **Vectorization**: Converts review text into embeddings, stored in FAISS for efficient retrieval.

### Query and Retrieve

FastAPI endpoints allow querying of review records based on keyword or product-specific searches, integrating Retriever-Augmented Generation to enhance responses.

### Monitoring and Metrics Collection

Prometheus is set up to track key metrics for API performance and query operations. Grafana dashboards provide visual insights to assess system health.

## Customization and Optional Batch Vectorization

The `vectorize_data.py` script can be run as a standalone batch vectorization process or configured as an optional step in the Docker setup for high-efficiency scenarios.

## Documentation

- **docs/**: Additional documentation files for each component and usage guidelines.

## License

This project is licensed under the MIT License.

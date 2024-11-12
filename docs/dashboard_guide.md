
# Dashboard Guide

This guide provides an overview of the **Streamlit** dashboard, along with instructions on using **Prometheus** and **Grafana** for system monitoring.

## 1. Streamlit Dashboard

The Streamlit dashboard enables users to interact with the Retriever-Augmented Generation (RAG) system, perform searches, and view feedback.

### Accessing the Dashboard

To access the dashboard, navigate to:
```plaintext
http://localhost:8501
```
Ensure that the `app` and `dashboard` services are running.

### Using the Dashboard

1. **Enter Query**:
   - Enter a text query in the sidebar to search for relevant reviews or records.
   - Optionally, specify filters like `Product Name` or `Product Type` to narrow the results.

2. **Set Filters**:
   - **Product Name** and **Product Type** fields allow specific filtering based on the product.

3. **View Results**:
   - Results will appear, displaying matched records with details like user review, product name, and country.
   - Rate the response with a rating slider if feedback functionality is enabled.

## 2. Prometheus

Prometheus collects and monitors metrics from the RAG system.

### Accessing Prometheus

Navigate to:
```plaintext
http://localhost:9090
```
Prometheus provides a powerful query interface for monitoring data.

### Key Metrics

- `http_requests_total`: Tracks the number of HTTP requests.
- `rag_records_processed_total`: Counts the records processed in the RAG pipeline.
- `response_times`: Measures response times across endpoints.

### Usage Tips

Use Prometheus's query interface to explore and visualize metrics over time. For advanced analysis, integrate Grafana to create custom visualizations.

## 3. Grafana

Grafana visualizes Prometheus metrics, allowing you to monitor system health.

### Accessing Grafana

Navigate to:
```plaintext
http://localhost:3000
```
Login with default credentials:
- **Username**: `admin`
- **Password**: `default123`

### Viewing Dashboards

Grafana has pre-configured dashboards for this project.

- **RAG Pipeline Dashboard**: View metrics like processing rate, request times, and system health.
- **Database and API Performance**: Monitor the database and API requests to identify potential bottlenecks.

### Configuring Alerts

You can set up alerts in Grafana for key metrics, such as response times or request rates, to proactively manage system performance.

For more details, refer to **monitoring_setup.md**.


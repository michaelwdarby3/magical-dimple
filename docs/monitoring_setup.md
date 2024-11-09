
# Monitoring Setup

This document provides instructions for setting up monitoring with Prometheus and Grafana to track system performance and metrics.

## Overview

Monitoring tools help track key metrics such as API response time, query rates, and feedback counts. This setup uses Prometheus for data collection and Grafana for visualization.

## Prometheus Setup

Prometheus collects metrics from the FastAPI application via an exposed `/metrics` endpoint.

1. **Configure Prometheus**: Edit `prometheus.yml` (located in `monitoring/`) to add the FastAPI app as a target.
2. **Start Prometheus**: Ensure Prometheus is included in `docker-compose.yml`.

### prometheus.yml Example

```yaml
scrape_configs:
  - job_name: "fastapi_app"
    scrape_interval: 5s
    static_configs:
      - targets: ["app:8000"]  # Update based on your service name and port
```

3. **Access Prometheus**: After starting, Prometheus is accessible at:
   ```plaintext
   http://localhost:9090
   ```

## Grafana Setup

Grafana visualizes metrics collected by Prometheus. Import pre-configured dashboards or create custom ones to track API and application metrics.

1. **Access Grafana**: Open Grafana at:
   ```plaintext
   http://localhost:3000
   ```
2. **Login**: Default credentials are `admin` / `admin`.
3. **Add Prometheus as a Data Source**:
   - Go to **Configuration > Data Sources > Add data source**.
   - Select **Prometheus** and set the URL to `http://prometheus:9090`.

4. **Import Dashboard**:
   - Go to **Create > Import**.
   - Use a pre-configured JSON file or Grafana's dashboard marketplace.

## Monitoring Metrics

- **API Response Time**: Tracks the average time for API requests to complete.
- **Query Rate**: Monitors the number of queries processed per second.
- **Feedback Counts**: Displays feedback ratings collected over time.

## Troubleshooting

- **No Data in Grafana**: Verify that Prometheus is collecting data and that the `/metrics` endpoint is accessible.
- **Connection Issues**: Check Docker networking settings and ensure all services are running.

This monitoring setup helps ensure the RAG system is performing efficiently and provides insights for optimizations.

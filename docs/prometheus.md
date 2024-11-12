
# Prometheus Monitoring Guide

## Overview

Prometheus is a powerful monitoring system used in this project to collect, store, and query metrics. 
In this setup, Prometheus scrapes and displays metrics from FastAPI and other services, 
allowing for detailed insight into application performance.

## Accessing Prometheus

Prometheus is accessible at [http://localhost:9090](http://localhost:9090) when running the project. 
You can perform queries, set up custom metrics, and inspect real-time data.

## Pre-configured Metrics

This setup includes several important pre-configured metrics for monitoring.

- **HTTP Request Count**: Tracks the total number of HTTP requests received by the FastAPI service.
- **Latency Metrics**: Measures request latency to monitor service responsiveness.
- **Error Rates**: Monitors the rate of errors to identify potential issues.

## Using Prometheus with FastAPI Metrics

FastAPI metrics are collected via Prometheus' HTTP scraping. The application exposes an endpoint (`/metrics`) 
where Prometheus retrieves all metrics data for monitoring.

Prometheus collects metrics at regular intervals, storing them for historical analysis.

### Sample Prometheus Queries

- **Total Requests**:
    ```
    http_requests_total
    ```

- **Error Rate Over Time**:
    ```
    increase(http_requests_total{status!~"2.."}[5m])
    ```

- **Average Latency**:
    ```
    rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m])
    ```

These queries are designed to give insight into the system's performance.

## Alerting Rules

Prometheus is configured with alerting rules located in the `fastapi_rules.yml` file.

### Example Alerts

- **High Latency Alert**: Triggers if request latency exceeds a threshold.
- **High Error Rate Alert**: Notifies when error rates increase beyond acceptable limits.

These alerts can be extended based on the needs of your project.

## Configuring Prometheus

Prometheus is configured via the `prometheus.yml` file in the `monitoring/prometheus` directory. 
To modify scraping intervals or target URLs, edit this configuration file.

For example, to adjust the scraping interval:

```yaml
scrape_interval: 15s
```

After making changes, restart Prometheus to apply the new settings.

## Troubleshooting

If Prometheus does not start correctly, check for issues in the configuration files. Common problems include:

- **Incorrect port mappings**: Ensure `9090:9090` is exposed in `docker-compose.yml`.
- **Endpoint issues**: Verify that the `/metrics` endpoint is reachable.

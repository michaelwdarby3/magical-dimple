# Grafana Dashboard
## Overview
This project includes a Grafana dashboard specifically configured to visualize metrics and monitor the health of the application. It connects to Prometheus for data retrieval and presents real-time metrics related to the FastAPI service, database, and user activity.

---

## Key Features
- Custom FastAPI Dashboard: Includes panels tailored to track FastAPI performance metrics, error rates, and user query statistics.
- Real-time Updates: Provides up-to-date monitoring of application health, aiding in proactive issue detection.
- Prometheus Integration: Leverages the Prometheus service to query and display relevant metrics.

---

## Accessing the Grafana Interface
To access Grafana, go to http://localhost:3000. The default login credentials are:

- Username: admin
- Password: default123

These credentials can be customized in your .env file or Docker configuration if needed.

---

## Viewing the Custom FastAPI Dashboard
Upon logging in, follow these steps to access the custom FastAPI dashboard:

1. In the Grafana interface, navigate to the sidebar.
2. Click on Dashboards > Manage.
3. Locate and select the FastAPI Dashboard (it may be listed under FastAPI Dashboards if organized by folder).

This dashboard includes panels for key metrics such as API response times, error rates, and database query activity.

If the FastAPI Dashboard is not visible, ensure that the fastapi_dashboard.json file is correctly located in the Grafana provisioning path (/etc/grafana/provisioning/dashboards/) and that the container is configured to load dashboards from this directory.

---

## Key Panels in the FastAPI Dashboard
- API Response Times: Visualizes average and maximum response times, helping identify latency issues.
- Error Rates: Tracks errors in the FastAPI service, alerting to potential issues with endpoints or data handling.
- Database Query Count: Displays the volume of database queries, offering insight into database load.
- User Query Volume: Monitors user activity over time, which is useful for understanding usage patterns or unexpected load spikes.

---

## Provisioning and Customization
The setup automatically provisions this dashboard from the /etc/grafana/provisioning/dashboards/ directory in the Docker container. For customization:

1. Go to the dashboard panel you wish to modify.
2. Edit queries, visualization types, or settings as needed.
3. Save any updates to maintain your preferred configurations.

---

## Additional Configuration
The Grafana service is configured to use:

- Custom JSON Dashboards: The fastapi_dashboard.json file is auto-loaded upon container startup.
- Provisioning Configuration: Located in provisioning/dashboards within the Grafana container, ensuring custom settings persist across restarts.
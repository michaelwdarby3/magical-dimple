# Project Title: Retriever-Augmented Generation System for Reviews and Recommendations

![Project Banner](assets/banner.png)

## Overview

This project is a full-stack **Retriever-Augmented Generation (RAG) system** that ingests data, stores it in a PostgreSQL database, and provides users with contextual information and recommendations through a FastAPI-powered API. The project includes a **Streamlit dashboard** for visualizing data, **monitoring tools** with Prometheus and Grafana, and **containerized services** for streamlined deployment with Docker.

## Features

- **Data Ingestion and Storage**: Load large datasets into PostgreSQL with automatic indexing for efficient querying.
- **Retriever-Augmented Generation (RAG)**: Use pre-trained models to generate contextually aware responses based on data.
- **Real-Time Monitoring**: Integrated monitoring with Prometheus and Grafana for tracking performance metrics.
- **Interactive Dashboard**: Visualize and interact with data using a Streamlit-based dashboard.
- **Dockerized Setup**: Multi-container setup with Docker Compose, including application, PostgreSQL, and monitoring services.

---

## Table of Contents

- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Dashboard](#dashboard)
- [Monitoring and Logging](#monitoring-and-logging)
- [Project Details](#project-details)
- [Contributing](#contributing)

---

## Project Structure

The project is organized for modularity and ease of navigation:

``` plaintext
project-root/
├── Dockerfile                   # Dockerfile for building the app container
├── docker-compose.yml           # Docker Compose file for managing services
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables for secure credentials
├── README.md                    # Project overview and instructions
│
├── src/                         # Main application source code
│   ├── main.py                  # Entry point for FastAPI app
│   ├── model/                   # Model loading, fine-tuning, and storage
│   ├── preprocessing/           # Data preprocessing scripts
│   ├── query/                   # Query and RAG pipeline handling
│   ├── utils/                   # General utility functions
│   ├── vectorization/           # Vectorization and embedding handling
│   └── queries/                 # SQL files for database queries
│
├── dashboard/                   # Streamlit dashboard files
│
├── tests/                       # Tests for application modules
│
├── docs/                        # Additional documentation
└── monitoring/                  # Monitoring setup files 
```

---

## Installation
### Prerequisites
Ensure that you have the following installed on your system:

- Docker and Docker Compose
- Python 3.9+

### Setup
1. Clone the Repository:

```bash
git clone https://github.com/yourusername/yourprojectname.git
cd yourprojectname 
```

2. Environment Variables: Configure your environment variables in a .env file. Here’s an example:

```plaintext
DB_NAME=review_database
DB_USER=data_scientist
DB_PASSWORD=default123
DB_HOST=db
DB_PORT=5432
```

3. Install Python Dependencies (if running locally without Docker):

```bash
pip install -r requirements.txt
```

4. Run Services with Docker Compose:

```bash
docker-compose up --build
```

5. Database Initialization:
- After starting the services, initialize the database by running the data ingestion script:

```bash
docker exec -it app_container python src/preprocessing/data_ingestion.py
```

---

## Usage
### API
The FastAPI server exposes various endpoints for querying and retrieving data. To explore all available endpoints, you can access the interactive documentation:

```plaintext
http://localhost:8000/docs
```

### Dashboard
The Streamlit dashboard provides an interactive interface for data visualization and analysis. Access it by navigating to:

```plaintext
http://localhost:8501
```

### Monitoring
Prometheus and Grafana are configured for monitoring and can be accessed at:
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

---

## API Documentation
Here’s a quick overview of key endpoints:


| Endpoint                    | Method | Description                                      |
|-----------------------------|--------|--------------------------------------------------|
| `/query/rag`                | POST   | Retrieve RAG-based response                      |
| `/data/users`               | GET    | Retrieve user information                        |
| `/data/reviews`             | GET    | Retrieve review information                      |
| `/feedback`                 | POST   | Submit feedback on RAG responses                 |


### Example Query
To retrieve a RAG response, you can send a POST request to /query/rag with JSON body:

```json
{
  "query": "What is the quality of service?",
  "top_k": 5
}
```

---

### Dashboard
The dashboard provides visualizations for data exploration and feedback tracking.

## Example Screenshots

---

## Monitoring and Logging
Prometheus and Grafana are configured for real-time monitoring, allowing you to track:

- API response times
- Query success/failure rates
- System resource usage
You can explore default metrics at http://localhost:9090 (Prometheus) and view visualizations on Grafana at http://localhost:3000.

---

## Project Details
### Data Ingestion
Data ingestion scripts load user and review data into PostgreSQL. Located in `src/preprocessing/data_ingestion.py`, this script reads CSV files and populates the database, ensuring a structured dataset for querying.

### Retriever-Augmented Generation (RAG)
The RAG pipeline integrates with a fine-tuned language model to generate responses based on user queries. The RAG logic is encapsulated in `src/query/rag_pipeline.py`.

### Model Management
Models are stored in the `src/models/` directory, with options for on-the-fly loading or fine-tuning.

### SQL Queries
Modular SQL queries are organized in src/queries/, allowing for easy management and reusability across the application.

---

## Contributing
We welcome contributions to improve this project! To contribute:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Make your changes and test thoroughly.
4. Submit a pull request.

---

### License
This project is licensed under the MIT License. See LICENSE for details.

---

### Contact
For questions or support, please reach out to michaelwdarby3.

# Data Ingestion Pipeline

This document describes the data ingestion pipeline, which is responsible for loading datasets into the PostgreSQL database.

## Overview

The data ingestion pipeline is designed to read data from CSV files, preprocess it, and load it into the database. This pipeline supports efficient data querying and retrieval.

## Running the Data Ingestion Script

To load data into the database, run the `data_ingestion.py` script. This script reads from CSV files and inserts data into the specified tables.

### Command

To run the ingestion script (from within the Docker container or environment):
```bash
python src/preprocessing/data_ingestion.py
```

## Expected CSV File Format

- **users.csv**: Should contain columns `user_id`, `name`, `age`, `country`.
- **reviews.csv**: Should contain columns `review_id`, `user_id`, `review_text`, `created_at`.
- **feedback.csv** (optional): Should contain `query`, `response`, `rating`, `created_at`.

## Error Handling and Troubleshooting

If there is an error during data ingestion, the script will display an error message. Ensure that the database is running and accessible, and verify the format of the CSV files.

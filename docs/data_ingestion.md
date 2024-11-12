
# Data Ingestion

This module handles the initial data ingestion for the LLM Data Engineering Project, supporting the loading of raw structured and unstructured data into the PostgreSQL database. The `data_ingestion.py` script is optional and can be used as a standalone utility to populate the database before other processes (such as vectorization) begin.

## Overview

Data ingestion is designed to take data from provided CSV files or JSON files and load them into the `users` and `reviews` tables. This process supports the following steps:
1. **Data Loading**: Reading data from files specified in the `/data` directory.
2. **Database Population**: Loading the structured data directly into PostgreSQL using the schema defined in `init.sql`.
3. **Preprocessing**: Ensuring that data loaded into the database is cleaned, well-structured, and ready for querying.

## Prerequisites

- **Database Setup**: Ensure that the PostgreSQL container is running and accessible. Use the `docker-compose.yml` setup provided to initiate the database service.
- **CSV Data**: Place the necessary CSV files (such as `users.csv` and `reviews.csv`) into the `/data` directory.
- **Environment Variables**: Database connection details must be set in the `.env` file, which `data_ingestion.py` will use for connectivity.

## Running Data Ingestion

To run the data ingestion process, you can execute the following command from the project root:

```bash
python src/data_ingestion.py
```

## Script Walkthrough

### 1. Loading Data from Files

The script begins by loading data from the `/data` directory, specifically reading `users.csv` and `reviews.csv` as sources.

### 2. Connecting to PostgreSQL

Using environment variables (`DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`), the script establishes a connection to the PostgreSQL instance.

### 3. Data Population

Data is inserted into the following tables:

- **`users`**: Contains user information, such as `user_id`, `name`, `age`, and `country`.
- **`reviews`**: Contains reviews linked to users, with fields for `review_id`, `user_id`, `review_text`, `product_name`, and `product_type`.

The script uses SQL `COPY` commands for efficient batch inserts.

## Notes on Usage

- **Optional Step**: Running `data_ingestion.py` is an optional part of the pipeline, intended for initial data loading or testing.
- **Updating Data**: If new data is added or schema changes are made, this script should be rerun to refresh the database contents.

## Troubleshooting

- **Connection Issues**: Ensure that the PostgreSQL service is running and accessible, with the correct credentials in `.env`.
- **Data Formatting Errors**: Validate the CSV files to ensure all fields conform to the required structure and contain no unexpected null values.

## Related Documentation

- **[Database Setup](database_setup.md)**: Details on database schema and setup.
- **[Vectorization](vectorization.md)**: Information on the vectorization process, which uses the ingested data.

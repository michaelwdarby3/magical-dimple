
# Database Setup

This document provides instructions for setting up the PostgreSQL database, configuring tables, and ensuring connectivity.

## Requirements

- **PostgreSQL**: Ensure PostgreSQL is installed and running.
- **Environment Variables**: Set up database credentials in a `.env` file in the project root.

## Database Initialization

1. **Start PostgreSQL**: Make sure your PostgreSQL server is running.
2. **Create Database**: Using psql or a database tool, create the database for this project.

### Example SQL Command

```sql
CREATE DATABASE review_database;
```

## Table Schema

Use the following SQL commands to create the required tables:

### Users Table

```sql
CREATE TABLE IF NOT EXISTS users (
    user_id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INT CHECK (age >= 0),
    country VARCHAR(100)
);
```

### Reviews Table

```sql
CREATE TABLE IF NOT EXISTS reviews (
    review_id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    review_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Feedback Table (Optional)

```sql
CREATE TABLE IF NOT EXISTS feedback (
    feedback_id SERIAL PRIMARY KEY,
    query TEXT,
    response TEXT,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Database Connection Settings

Update your `.env` file with database connection details:

```plaintext
DB_NAME=review_database
DB_USER=data_scientist
DB_PASSWORD=default123
DB_HOST=db
DB_PORT=5432
```

Ensure these settings match the configuration in your `docker-compose.yml` and FastAPI `db_utils.py`.

## Troubleshooting

- **Connection Refused**: Verify PostgreSQL is running and accessible at the specified host and port.
- **Permissions Issues**: Ensure the user has appropriate permissions on the database.

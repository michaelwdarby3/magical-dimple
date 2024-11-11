#!/bin/bash

# Wait for the database to be ready
echo "Checking database connection..."

# Loop until the database is reachable by trying to connect with psql
until PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c '\q' 2>/dev/null; do
  echo "Waiting for database connection..."
  sleep 5  # Wait before retrying
done

echo "Database is ready. Starting app..."
exec uvicorn src.main:app --host 0.0.0.0 --port 8000

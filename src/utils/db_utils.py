import os
import psycopg2

def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME", "review_database"),
        user=os.getenv("DB_USER", "data_scientist"),
        password=os.getenv("DB_PASSWORD", "default123"),
        host=os.getenv("DB_HOST", "db"),  # 'db' refers to the db service in Docker Compose
        port=os.getenv("DB_PORT", "5432")
    )

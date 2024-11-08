# src/data_ingestion.py
import pandas as pd
from src.utils.db_utils import get_db_connection
import psycopg2

def load_data(file_path):
    """Loads data from a CSV file into a DataFrame."""
    return pd.read_csv(file_path)

def insert_data_into_table(dataframe, table_name, columns):
    """Inserts DataFrame records into a specified PostgreSQL table."""
    connection = get_db_connection()
    cursor = connection.cursor()

    # Convert DataFrame rows to list of tuples for insertion
    records = [tuple(row) for row in dataframe[columns].values]

    # Generate placeholders based on the number of columns
    placeholders = ", ".join(["%s"] * len(columns))
    insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"

    try:
        cursor.executemany(insert_query, records)
        connection.commit()
        print(f"Data successfully inserted into {table_name}")
    except Exception as e:
        print(f"Error inserting data into {table_name}: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

def load_users(file_path):
    """Loads users from CSV into the database."""
    users_df = load_data(file_path)
    insert_data_into_table(users_df, "users", ["user_id", "name", "age", "country"])


def load_reviews(file_path):
    """Loads reviews from CSV into the database."""
    reviews_df = load_data(file_path)
    insert_data_into_table(reviews_df, "reviews", ["review_id", "user_id", "review_text", "created_at"])

# Run the loading functions
if __name__ == "__main__":
    load_users("../../data/users.csv")
    load_reviews("../../data/reviews.csv")

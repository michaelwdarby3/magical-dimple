import re
import pandas as pd
from datetime import datetime
from src.utils.log_utils import setup_logger

# Initialize logging
logger = setup_logger("preprocessing")


def clean_text(text):
    """Basic text cleaning function."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra whitespace
    return text


def handle_missing_values(df):
    """Handle missing values in the dataframe."""
    # Fill missing values for each column based on data type
    df['age'].fillna(df['age'].median(), inplace=True)  # Numeric: use median
    df['country'].fillna('Unknown', inplace=True)  # Categorical: use placeholder
    df['user_review'].fillna('', inplace=True)  # Text: empty string
    return df


def standardize_dates(df, date_column):
    """Convert dates to a consistent format."""
    df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
    return df


def preprocess_data(data_path):
    """Main function to load, clean, and preprocess data."""
    logger.info("Starting data preprocessing...")

    # Load data
    df = pd.read_json(data_path)

    # Apply text cleaning
    df['user_review'] = df['user_review'].apply(clean_text)

    # Handle missing values
    df = handle_missing_values(df)

    # Standardize dates
    df = standardize_dates(df, 'signup_date')

    logger.info("Data preprocessing completed.")
    return df


# Example of using the function
if __name__ == "__main__":
    preprocessed_data = preprocess_data('data/sample_data.json')
    preprocessed_data.to_json('data/preprocessed_data.json', orient='records', lines=True)

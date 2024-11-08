import os
import json
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env if needed
def load_env():
    """Load environment variables from a .env file."""
    load_dotenv()

def read_csv(file_path):
    """Read a CSV file and return it as a DataFrame."""
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading CSV file at {file_path}: {e}")
        return None

def save_csv(dataframe, file_path):
    """Save a DataFrame to a CSV file."""
    try:
        dataframe.to_csv(file_path, index=False)
        print(f"Data saved to {file_path}")
    except Exception as e:
        print(f"Error saving DataFrame to CSV at {file_path}: {e}")

def read_json(file_path):
    """Read a JSON file and return the parsed content."""
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"Error reading JSON file at {file_path}: {e}")
        return None

def save_json(data, file_path):
    """Save data to a JSON file."""
    try:
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Data saved to {file_path}")
    except Exception as e:
        print(f"Error saving data to JSON at {file_path}: {e}")

def ensure_directory_exists(directory_path):
    """Ensure that a directory exists, creating it if necessary."""
    Path(directory_path).mkdir(parents=True, exist_ok=True)

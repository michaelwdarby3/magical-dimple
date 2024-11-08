from src.preprocessing.preprocess_data import clean_text, handle_missing_values
import pandas as pd

def test_clean_text():
    assert clean_text("Hello, World!") == "hello world"
    assert clean_text("Test!!!") == "test"

def test_handle_missing_values():
    df = pd.DataFrame({"age": [25, None, 35], "country": ["USA", None, "Canada"]})
    df = handle_missing_values(df)
    assert df["age"].isnull().sum() == 0
    assert df["country"].isnull().sum() == 0

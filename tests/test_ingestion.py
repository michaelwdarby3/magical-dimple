import pytest
from src.ingestion.ingest_data import load_data, insert_data_into_db

def test_load_data():
    data = load_data("data/sample_data.json")
    assert len(data) > 0
    assert "user_id" in data[0]

@pytest.mark.parametrize("input_data, expected_result", [
    ({"name": "John", "age": 25}, True),
    ({"name": "", "age": None}, False),
])
def test_insert_data_into_db(mocker, input_data, expected_result):
    # Mock the database connection and cursor
    mock_cursor = mocker.Mock()
    mock_conn = mocker.Mock()
    mock_conn.cursor.return_value = mock_cursor

    result = insert_data_into_db(input_data, mock_conn)
    assert result == expected_result

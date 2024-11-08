import requests
import pandas as pd

API_BASE_URL = "http://localhost:8000"  # Adjust this if running on a different host/port

def fetch_rag_response(query, top_k):
    """Fetches a RAG-generated response from the API."""
    url = f"{API_BASE_URL}/query/rag"
    payload = {"query": query, "top_k": top_k}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching RAG response: {e}")
        return {}

def fetch_feedback_summary():
    """Fetches feedback summary data from the API."""
    url = f"{API_BASE_URL}/feedback/summary"
    try:
        response = requests.get(url)
        response.raise_for_status()
        feedback_data = response.json()
        # Convert to DataFrame for easy handling in Streamlit
        return pd.DataFrame(feedback_data)
    except requests.RequestException as e:
        print(f"Error fetching feedback summary: {e}")
        return pd.DataFrame()

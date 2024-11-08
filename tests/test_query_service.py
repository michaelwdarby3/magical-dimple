from fastapi.testclient import TestClient
from src.query.query_service import app

client = TestClient(app)

def test_query_endpoint():
    response = client.post("/query/", json={"query": "test query", "top_k": 5})
    assert response.status_code == 200
    assert "similar_records" in response.json()

def test_rag_endpoint():
    response = client.post("/rag/", json={"query": "test query", "top_k": 5})
    assert response.status_code == 200
    assert "response" in response.json()

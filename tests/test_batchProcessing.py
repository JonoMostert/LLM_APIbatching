from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_batch_processing_multiple_queries():
    """ Test if multiple queries are correctly batched and processed. """
    queries = [
        {"query": "Define machine learning."},
        {"query": "Explain quantum computing."}
    ]

    responses = [client.post("/query", json=q) for q in queries]

    for response, query in zip(responses, queries):
        assert response.status_code == 200
        assert "result" in response.json()
        assert response.json()["result"] == f"Processed: {query['query']}"

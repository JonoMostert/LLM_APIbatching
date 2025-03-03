import pytest
import logging
from fastapi.testclient import TestClient
from main import app

# Configure logging for tests
# logging.basicConfig(level=logging.DEBUG, force=True)
# logger = logging.getLogger(__name__)

client = TestClient(app)

def test_query_processing():
    """ Test if the microservice correctly batches and processes queries. """

    # logger.debug("Starting test: test_query_processing")

    # Send the query request
    response = client.post("/query", json={"query": "What is AI?"})

    # Ensure request was accepted
    assert response.status_code == 200
    # logger.debug("Query request accepted. Checking response...")

    # Fetch the response result
    processed_result = response.json().get("result")
    # logger.debug(f"Test result response: {processed_result}")

    # Ensure the response contains the processed query result
    assert processed_result == "Processed: What is AI?"


def test_invalid_query():
    """ Test sending an empty query string. """
    response = client.post("/query", json={"query": ""})
    assert response.status_code == 422

def test_large_query():
    """ Test handling of a very large query string. """
    large_query = "A" * 5000  # Exceeding normal size
    response = client.post("/query", json={"query": large_query})
    assert response.status_code == 200
    assert "result" in response.json()
    assert response.json()["result"] == f"Processed: {large_query}"

def test_rapid_queries():
    """ Test how the system handles a rapid queries. """
    queries = [{"query": f"Test {i}"} for i in range(10)]
    responses = [client.post("/query", json=q) for q in queries]

    for response, query in zip(responses, queries):
        assert response.status_code == 200
        assert "result" in response.json()
        assert response.json()["result"] == f"Processed: {query['query']}"


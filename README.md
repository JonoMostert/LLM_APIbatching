# LLM Query Batching Microservice

## Overview
This is a FastAPI microservice that accepts queries via an HTTP API, batches them efficiently, and sends them to a **mocked Large Language Model (LLM) API** for processing.

The service:
- Collects incoming queries into an async queue.
- Processes them in batches at a fixed interval.
- Returns results to clients once processing is complete.
- Includes a health check endpoint.
- Provides a suite of unit tests for validation.

---

## Running the service locally

### **1️. Prerequisites**
Ensure you have the following installed:
- **Python 3.8+**

### **2. Set up Virtual Env**
```sh
python -m venv venv
venv\Scripts\activate
```

### **3. Install dependancies**
```sh
pip install -r requirements.txt
```
### **4. Run service locally**
The script is set up to run the server, so simply type:
```sh
python main.py
```
If you wish to run the server in reload mode:
```sh
uvicorn main:app --reload
```
By default, Uvicorn runs on 127.0.0.1:8000 (localhost)
To run on a different port, simply use (as an example):
```sh
uvicorn main:app --host 0.0.0.0 --port 5000 --reload
```
* Ensure that the POST request is sent to the correct base URL

### **5. Send request using Postman**
POST request to endpoint: http://127.0.0.1:5000/query 

Body:
`{"query": "What is AI?"}`

Expected response:
`{"result": "Processed: What is AI?"}`

## Running test suite locally
Assuming previous steps from 1 to 3 were completed in "Running the service locally"
```sh
pytest tests/
```
There is a CI file that will make the tests run with every GitHub commit

## Next Steps

**Current Implementation**
- I use multithreading (threading.Thread) for batch processing
- This is because the main workload is I/O-bound (waiting for queries and responses)
- Threads are better when tasks involve waiting (API calls, network requests etc)

**Actual Implementation of LLM**
If the mock LLM were replaced with a real one (involving CPU intensive tasks), then one would use multiprocessing for the batching of queries:
- Replace threading.Thread with multiprocessing.Process
- Use multiprocessing.Queue() instead of asyncio.Queue()

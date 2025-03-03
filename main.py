from fastapi import FastAPI, HTTPException  
import asyncio
from pydantic import BaseModel
from typing import List, Dict, Tuple
import logging
import threading
from functions import batch_processor, query_queue, results
import uvicorn

# Configure logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)

app = FastAPI()

# Configurable batch processing interval (seconds)
BATCH_INTERVAL = 5

waiting_clients: Dict[int, threading.Event] = {}  # Tracks waiting clients in batch processor function
query_counter = 0  # Unique ID counter for queries

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def receive_query(request: QueryRequest):
    """ Accepts a query and waits until it's processed before returning the response. """
    global query_counter

    # Ensure that an empty request is not sent
    if not request.query.strip():
        raise HTTPException(status_code=422, detail="Query cannot be empty")
    
    query_id = query_counter
    query_counter += 1

    # logger.debug(f"Received query {query_id}: {request.query}")

    # Create an event that will be set when processing is complete    
    if query_id not in waiting_clients:
        waiting_clients[query_id] = threading.Event() # Used threading.Event for a trigger once background task is compplete

    # Put the query in the queue
    await query_queue.put((query_id, request.query))

    # logger.debug(f"Query {query_id} added to queue. Waiting for processing...")
    
    # Wait for processing to complete
    waiting_clients[query_id].wait()

    result = results.pop(query_id, None)
    # logger.debug(f"Returning result for query {query_id}: {result}")
    
    # Retrieve the result and return it
    return {"result": result}

@app.get("/health")
async def health_check():
    return {"status": "ok"}


threading.Thread(target=batch_processor, args=(waiting_clients, BATCH_INTERVAL), daemon=True).start()
# logger.debug("Batch processor thread has been initialized.")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000, reload=False)
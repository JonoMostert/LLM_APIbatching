import asyncio
import logging
from typing import List, Tuple, Dict
import threading

# Configure logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)

# Dictionary to store processed results
results: Dict[int, str] = {}

# Queue for batch processing
query_queue = asyncio.Queue()


def batch_processor(waiting_clients: Dict[int, threading.Event], batch_interval):
    """Runs batch processing every `batch_interval` seconds in a background thread."""
    # logger.debug("Batch processor thread started...")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def process_batches():
        while True:
            await asyncio.sleep(batch_interval)

            batch: List[Tuple[int, str]] = []
            while not query_queue.empty():
                item = await query_queue.get()
                batch.append(item)
                # logger.debug(f"Processing query {item}")

            if batch:
                processed_results = await mock_llm_api([q[1] for q in batch])
                for (query_id, _), result in zip(batch, processed_results):
                    results[query_id] = result
                    # logger.debug(f"Query {query_id} processed: {result}")

                    if query_id in waiting_clients:
                        # logger.debug(f"Notifying waiting client for query {query_id}")
                        waiting_clients[query_id].set()
                        del waiting_clients[query_id]

    loop.run_until_complete(process_batches())


async def mock_llm_api(queries: List[str]) -> List[str]:
    """Simulates LLM processing with a delay and returns dummy responses."""
    # logger.debug(f"Mock LLM API received queries: {queries}")
    await asyncio.sleep(1)  # Simulate processing delay
    return [f"Processed: {query}" for query in queries]

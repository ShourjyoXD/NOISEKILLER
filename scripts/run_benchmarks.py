import asyncio
import httpx
import time
import statistics
from typing import List

# Configuration
API_URL = "http://127.0.0.1:8000/api/v1/verify"
CONCURRENT_REQUESTS = 5  # Simulating multiple users
TOTAL_TESTS = 20

async def benchmark_request(client: httpx.AsyncClient, test_id: int):
    payload = {
        "query": f"Test Query #{test_id}: Calculate the risk of shadow IT in cloud security.",
        "context": "Shadow IT refers to IT systems built and used within organizations without explicit organizational approval."
    }
    
    start = time.perf_counter()
    try:
        response = await client.post(API_URL, json=payload, timeout=30.0)
        end = time.perf_counter()
        
        if response.status_code == 200:
            data = response.json()
            return {
                "total_time": end - start,
                "engine_time": data.get("execution_time_ms", 0) / 1000,
                "verified": data.get("verified"),
                "score": data.get("confidence_score")
            }
    except Exception as e:
        print(f"Request {test_id} failed: {e}")
    return None

async def run_suite():
    print(f"Starting NOISEKILLER Benchmark Suite ({TOTAL_TESTS} total requests)...")
    
    async with httpx.AsyncClient() as client:
        tasks = [benchmark_request(client, i) for i in range(TOTAL_TESTS)]
        results = await asyncio.gather(*tasks)
    
    # Filter out failed requests
    valid_results = [r for r in results if r is not None]
    
    if not valid_results:
        print("All benchmark requests failed. Is the server running?")
        return

    # Calculate Metrics
    latencies = [r["total_time"] for r in valid_results]
    engine_times = [r["engine_time"] for r in valid_results]
    
    print("\nNOISEKILLER PERFORMANCE REPORT")
    print(f"Total Requests: {len(valid_results)}/{TOTAL_TESTS}")
    print(f"Average E2E Latency: {statistics.mean(latencies):.2f}s")
    print(f"P95 Latency (Worst Case): {statistics.quantiles(latencies, n=20)[18]:.2f}s")
    print(f"Average Engine Processing: {statistics.mean(engine_times):.2f}s")
    print(f"Verification Success Rate: {(sum(1 for r in valid_results if r['verified']) / len(valid_results)) * 100}%")
    print("------------------------------------------\n")

if __name__ == "__main__":
    asyncio.run(run_suite())
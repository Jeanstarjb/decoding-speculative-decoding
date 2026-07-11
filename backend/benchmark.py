import time
import requests
import concurrent.futures
import statistics

API_URL = "http://localhost:8000/api/inference"

# Configuration for benchmarking
NUM_REQUESTS = 100
CONCURRENT_REQUESTS = 10
INPUT_TEXT = "The quick brown fox jumps over the lazy dog."
MAX_TOKENS = 50

def send_request():
    payload = {"input_text": INPUT_TEXT, "max_tokens": MAX_TOKENS}
    try:
        start_time = time.time()
        response = requests.post(API_URL, json=payload)
        response_time = time.time() - start_time
        if response.status_code == 200:
            return response_time
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(f"Request failed: {e}")
        return None

def main():
    response_times = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENT_REQUESTS) as executor:
        futures = [executor.submit(send_request) for _ in range(NUM_REQUESTS)]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result is not None:
                response_times.append(result)

    if response_times:
        avg_time = statistics.mean(response_times)
        p95_time = statistics.quantiles(response_times, n=20)[18]  # 95th percentile
        print(f"Total Requests: {NUM_REQUESTS}")
        print(f"Successful Requests: {len(response_times)}")
        print(f"Average Response Time: {avg_time:.2f} seconds")
        print(f"95th Percentile Response Time: {p95_time:.2f} seconds")
    else:
        print("No successful requests.")

if __name__ == "__main__":
    main()
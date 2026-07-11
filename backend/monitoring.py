import logging
import time
from prometheus_client import Counter, Histogram

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("inference_monitor")

# Prometheus metrics
REQUEST_COUNT = Counter(
    'inference_request_count',
    'Total number of inference requests',
    ['endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'inference_request_latency_seconds',
    'Latency of inference requests in seconds',
    ['endpoint']
)

ERROR_COUNT = Counter(
    'inference_error_count',
    'Total number of inference errors',
    ['endpoint', 'error_type']
)

def log_request(endpoint: str, status: str, start_time: float):
    """
    Logs and tracks metrics for an inference request.

    Args:
        endpoint (str): The API endpoint being called.
        status (str): The status of the request (e.g., 'success', 'failure').
        start_time (float): The start time of the request.
    """
    duration = time.time() - start_time
    REQUEST_COUNT.labels(endpoint=endpoint, status=status).inc()
    REQUEST_LATENCY.labels(endpoint=endpoint).observe(duration)
    logger.info(f"Endpoint: {endpoint}, Status: {status}, Latency: {duration:.4f} seconds")

def log_error(endpoint: str, error_type: str):
    """
    Logs and tracks metrics for an error.

    Args:
        endpoint (str): The API endpoint where the error occurred.
        error_type (str): The type of error that occurred.
    """
    ERROR_COUNT.labels(endpoint=endpoint, error_type=error_type).inc()
    logger.error(f"Endpoint: {endpoint}, Error: {error_type}")
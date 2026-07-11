from prometheus_client import Gauge
from datetime import datetime
import threading
import time

class BenchmarkMetrics:
    def __init__(self):
        self.avg_response_time = Gauge('benchmark_avg_response_time', 'Average response time in seconds')
        self.p95_response_time = Gauge('benchmark_p95_response_time', '95th percentile response time in seconds')
        self.timestamps = []
        self.avg_response_times = []
        self.p95_response_times = []
        self.lock = threading.Lock()

    def update_metrics(self, avg_time, p95_time):
        with self.lock:
            timestamp = datetime.now().strftime('%H:%M:%S')
            self.timestamps.append(timestamp)
            self.avg_response_times.append(avg_time)
            self.p95_response_times.append(p95_time)
            self.avg_response_time.set(avg_time)
            self.p95_response_time.set(p95_time)

    def get_metrics(self):
        with self.lock:
            return {
                'timestamps': self.timestamps,
                'avgResponseTimes': self.avg_response_times,
                'p95ResponseTimes': self.p95_response_times,
            }

benchmark_metrics = BenchmarkMetrics()

def start_metrics_updater():
    def update_loop():
        while True:
            # Simulate updating metrics every 10 seconds
            time.sleep(10)
            # Replace the following with real benchmarking data
            avg_time = 0.5  # Placeholder
            p95_time = 0.8  # Placeholder
            benchmark_metrics.update_metrics(avg_time, p95_time)

    threading.Thread(target=update_loop, daemon=True).start()
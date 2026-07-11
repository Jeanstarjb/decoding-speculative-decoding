# Decoding Speculative Decoding

**Research Paper:** [https://arxiv.org/pdf/2402.01528v4](https://arxiv.org/pdf/2402.01528v4)

## The Mission
Large Language Models (LLMs) are computationally expensive and resource-intensive, limiting their accessibility and scalability for real-world applications such as education, healthcare, and customer support. This hinders the democratization of AI and its potential to benefit society broadly.

## Architecture
The solution involves building a scalable, production-ready inference system that leverages speculative decoding to speed up LLM inference. The architecture will use a two-model system: a lightweight, hardware-efficient draft model for speculative token generation and a larger target LLM for verification. The tech stack includes Python, PyTorch for model integration, TensorRT for hardware optimization, FastAPI for serving the models, Redis for caching, Docker for containerization, and Kubernetes for orchestration.

## Monitoring and Logging
A robust monitoring and logging system has been implemented using Prometheus and Python's logging library. The system tracks:

- **Inference Latency:** Measures the time taken for each inference request.
- **Throughput:** Tracks the total number of requests processed.
- **Errors:** Logs errors and tracks their occurrence.

### Metrics Endpoint
The Prometheus metrics are exposed at the `/metrics` endpoint. You can access this endpoint at `http://localhost:9100/metrics` when running locally.

### Setting Up Prometheus
1. Ensure Docker and Docker Compose are installed on your machine.
2. Start the services using the following command:

   ```bash
   docker-compose up --build
   ```

3. Access the Prometheus dashboard at `http://localhost:9090`.
4. Add the `speculative_decoding_api` job to your Prometheus targets to monitor the API.

## Progress Log
- [x] Initial repository setup
- [x] Implement draft model integration
- [x] Implement target model verification
- [x] Add speculative decoding logic
- [x] Optimize with TensorRT
- [x] Set up FastAPI for serving
- [x] Integrate Redis caching
- [x] Create Docker containerization
- [x] Configure Kubernetes for orchestration
- [x] Implement monitoring and logging system

- **Completed Task:** Set up the project repository with basic folder structure, README, and initial configurations.
- **Completed Task:** Create Dockerfiles for both the draft model and target LLM, ensuring compatibility with TensorRT and GPU acceleration.
- **Completed Task:** Implement the draft model selection logic based on the research insights to optimize for latency and hardware efficiency.
- **Completed Task:** Develop the speculative decoding algorithm, including speculative token generation by the draft model and verification by the target LLM.
- **Completed Task:** Integrate the draft model and target LLM into a unified inference pipeline using PyTorch and FastAPI.
- **Completed Task:** Implement caching mechanisms using Redis to store and retrieve speculative tokens for faster inference.
- **Completed Task:** Implement monitoring and logging system to track inference latency, throughput, and errors in real-time.
- **Completed Task:** Design and implement a monitoring and logging system to track inference latency, throughput, and errors in real time.
- **Completed Task:** Develop a hardware optimization module using TensorRT to accelerate the draft model's performance on GPUs.
- **Completed Task:** Build a REST API using FastAPI to expose the inference system for external applications.
- **Completed Task:** Create unit tests and integration tests for the speculative decoding pipeline to ensure robustness and correctness.
- **Completed Task:** Develop a user-facing dashboard for visualizing system performance metrics and monitoring hardware utilization.
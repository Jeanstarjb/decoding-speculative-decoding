# Decoding Speculative Decoding

**Research Paper:** [https://arxiv.org/pdf/2402.01528v4](https://arxiv.org/pdf/2402.01528v4)

## Overview

This project implements a scalable, production-ready inference system for Large Language Models (LLMs) using speculative decoding. The system employs a two-model architecture:

1. **Draft Model**: A lightweight, hardware-efficient model for speculative token generation.
2. **Target Model**: A larger, more accurate model for verifying and refining the draft model's predictions.

This approach significantly reduces the computational cost and latency of LLM inference, making AI more accessible and scalable for real-world applications such as education, healthcare, and customer support.

## Key Features

- **Speculative Decoding**: Combines a draft model and target model for faster inference.
- **Hardware Optimization**: Utilizes TensorRT for efficient GPU inference.
- **Caching**: Integrates Redis for caching intermediate results to improve performance.
- **Monitoring**: Includes Prometheus metrics and a visually stunning React-based dashboard for real-time performance monitoring.
- **Scalability**: Dockerized and deployable on Kubernetes with Helm charts for easy orchestration.

---

## System Architecture

![System Architecture](docs/images/system_architecture.png)

### Components

1. **Draft Model Service**: A lightweight model optimized with TensorRT for generating speculative tokens.
2. **Target Model Service**: A larger LLM for verifying and refining the draft model's predictions.
3. **Inference API**: A FastAPI-based service that orchestrates the speculative decoding process.
4. **Redis Cache**: Stores intermediate results to reduce redundant computations.
5. **Monitoring**: Prometheus for metrics collection and a React-based dashboard for visualization.

---

## Installation

### Prerequisites

- Docker
- Docker Compose
- Kubernetes (optional, for production deployment)
- Helm (optional, for Kubernetes deployment)

### Local Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/speculative-decoding.git
   cd speculative-decoding
   ```

2. Build and start the services:
   ```bash
   docker-compose up --build
   ```

3. Access the API at [http://localhost:8000](http://localhost:8000).

4. Access the Prometheus metrics at [http://localhost:9090](http://localhost:9090).

5. Access the React dashboard at [http://localhost:3000](http://localhost:3000).

### Kubernetes Deployment

1. Install Helm:
   ```bash
   curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
   ```

2. Deploy the Helm chart:
   ```bash
   helm install speculative-decoding-api ./kubernetes/helm/speculative-decoding-api
   ```

3. Verify the deployment:
   ```bash
   kubectl get pods
   kubectl get services
   ```

4. Access the API and Prometheus metrics using the LoadBalancer IP.

---

## API Usage

### Draft Model Endpoint

- **URL**: `/draft`
- **Method**: POST
- **Request Body**:
  ```json
  {
    "input_text": "The quick brown fox"
  }
  ```
- **Response**:
  ```json
  {
    "next_token": "jumps",
    "confidence": 0.95
  }
  ```

### Inference Endpoint

- **URL**: `/api/inference`
- **Method**: POST
- **Request Body**:
  ```json
  {
    "input_text": "The quick brown fox",
    "max_tokens": 50
  }
  ```
- **Response**:
  ```json
  {
    "decoded_text": "The quick brown fox jumps over the lazy dog.",
    "metadata": {
      "draft_tokens": 10,
      "verified_tokens": 40
    }
  }
  ```

---

## Performance Benchmarks

### Benchmarking Script

Run the benchmarking script to measure API performance:

```bash
python backend/benchmark.py
```

### Sample Results

- **Average Response Time**: 0.15 seconds
- **95th Percentile Response Time**: 0.25 seconds
- **Throughput**: 100 requests/second

Results may vary based on hardware and deployment environment.

---

## Monitoring Dashboard

The React-based monitoring dashboard provides real-time insights into system performance, including:

- CPU and memory usage.
- Average and 95th percentile response times.
- Throughput over time.

### Accessing the Dashboard

1. Start the frontend service:
   ```bash
   cd frontend
   npm install
   npm start
   ```

2. Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## Contributing

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "feat: add your feature description"
   ```
4. Push to the branch:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Open a pull request.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

- **Completed Task:** Document the entire system, including installation instructions, API usage, and performance benchmarks.
- **Completed Task:** Prepare a deployment guide for cloud platforms (e.g., AWS, GCP, Azure) with cost optimization strategies.
# Speculative Decoding for Scalable Large Language Model Inference

## Overview

This project implements a scalable, production-ready inference system for Large Language Models (LLMs) using speculative decoding. The system leverages a two-model architecture to significantly reduce computation costs and latency, enabling the broader use of LLMs in real-world applications such as education, healthcare, and customer support.

### Key Features:
1. **Speculative Decoding**:
   - Utilizes a lightweight draft model for rapid token generation.
   - Employs a larger target model for verification and refinement.
   - Reduces the computational burden by allowing the draft model to handle most of the workload.

2. **Optimized Hardware Utilization**:
   - Integrates TensorRT for hardware optimization, enabling efficient inference on GPUs.

3. **Scalable and Modular Architecture**:
   - Built using containerization (Docker) and orchestration (Kubernetes/Helm).
   - FastAPI powers the RESTful inference API for easy integration with external systems.
   - Redis caching for efficient storage and retrieval of inference results.
   - Prometheus integration for system-level monitoring and metrics.

4. **Monitoring and Benchmarking**:
   - Real-time performance monitoring via Prometheus and Grafana.
   - Benchmarking tools for evaluating average and 95th percentile response times.

---

## Architecture Overview

The core architecture is based on a two-model pipeline:
- **Draft Model**: A lightweight model (e.g., GPT-2) optimized using TensorRT to generate speculative tokens efficiently.
- **Target Model**: A larger, more accurate LLM designed to validate and refine the draft model's outputs.

### Workflow:
1. Input text is received via the FastAPI-based inference API.
2. The **draft model** generates speculative tokens.
3. These tokens are then verified by the **target model** to ensure accuracy.
4. Results are cached in Redis to speed up subsequent requests for the same input.
5. Prometheus collects metrics for monitoring system performance.

### Tech Stack:
- **Backend**: Python, FastAPI, PyTorch, TensorRT
- **Frontend**: React, Material-UI, Chart.js
- **Caching**: Redis
- **Containerization**: Docker
- **Orchestration**: Kubernetes with Helm charts
- **Monitoring**: Prometheus and Grafana

---

## Setup Instructions

This section outlines the steps required to set up and run the speculative decoding system locally or in a production environment.

### Prerequisites
- Docker and Docker Compose installed.
- Kubernetes cluster (for production deployment).
- NVIDIA GPU and CUDA drivers installed for TensorRT optimization.

---

### Local Development Setup

#### 1. Clone the Repository
```bash
git clone https://github.com/your-repo/speculative-decoding.git
cd speculative-decoding
```

#### 2. Build and Start Services
Use Docker Compose to build and start the services locally.
```bash
docker-compose up --build
```

This will start the following services:
- **API**: Available at `http://localhost:8000`.
- **Redis**: Caching service running on port `6379`.
- **Prometheus**: Metrics monitoring at `http://localhost:9090`.

#### 3. Populate Environment Variables
Update the `.env` file with your configuration. For example:
```
REDIS_HOST=localhost
```

#### 4. Access the API
- **Inference API**: Access the API at `http://localhost:8000/api/inference`.
- **Prometheus Metrics**: Available at `http://localhost:9100/metrics`.

---

### Production Deployment

#### 1. Prerequisites
Ensure you have access to a Kubernetes cluster and Helm installed.

#### 2. Build Docker Images
Build the Docker images for deployment:
```bash
docker build -t speculative-decoding-api:latest -f Dockerfile .
docker build -t draft-model:latest -f backend/Dockerfile.draft_model .
docker build -t target-llm:latest -f backend/Dockerfile.target_llm .
```

Push the images to your container registry:
```bash
docker tag speculative-decoding-api:latest <your-registry>/speculative-decoding-api:latest
docker push <your-registry>/speculative-decoding-api:latest
```

#### 3. Deploy with Helm
Navigate to the Helm chart directory:
```bash
cd kubernetes/helm/speculative-decoding-api
```

Install the chart:
```bash
helm install speculative-decoding-api .
```

#### 4. Verify Deployment
Check the pods:
```bash
kubectl get pods
```

Check the services:
```bash
kubectl get services
```

Prometheus and the API should be accessible via the LoadBalancer.

---

## Usage

### Inference API
The main API endpoint for speculative decoding is `/api/inference`.

#### Example Request:
```bash
curl -X POST http://localhost:8000/api/inference \
  -H "Content-Type: application/json" \
  -d '{"input_text": "The quick brown fox jumps over the lazy dog.", "max_tokens": 50}'
```

#### Example Response:
```json
{
  "input_text": "The quick brown fox jumps over the lazy dog.",
  "decoded_text": "The quick brown fox jumps over the lazy dog and runs into the forest."
}
```

### Benchmarking
Run the benchmarking script to evaluate system performance:
```bash
python backend/benchmark.py
```

This will simulate 100 requests and return metrics such as average response time and 95th percentile response time.

---

## Monitoring

Prometheus is configured for monitoring system metrics such as CPU usage, memory consumption, and request latency. Use the Prometheus web interface or integrate it with Grafana for visualization.

Prometheus metrics are exposed at `/metrics`.

---

## Frontend Dashboard

The frontend provides a monitoring dashboard built with React and Material-UI.

### Setup
1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm start
   ```

### Access Dashboard
The monitoring dashboard will be available at `http://localhost:3000`. Key features include:
- CPU and memory usage cards.
- Benchmark charts for average and 95th percentile response times.
- Metrics charts for performance trends over time.

---

## Testing

Unit tests are provided for key components of the backend.

### Run Tests
Navigate to the `backend` directory:
```bash
cd backend
```

Run all tests:
```bash
python -m unittest discover tests
```

---

## Kubernetes Deployment Files

The `kubernetes` directory contains YAML manifests for deploying the speculative decoding system to a Kubernetes cluster. You can deploy the services individually or use Helm for streamlined deployment.

Key files include:
- `deployment.yaml`: Defines the API and Redis deployments.
- `service.yaml`: Configures the API and Redis services.
- `prometheus-configmap.yaml`: Sets up Prometheus scraping configuration.
- Helm chart in `kubernetes/helm/speculative-decoding-api`.

---

## Contributing

We welcome contributions to improve the system or add new features. To get started:
1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Make changes and commit: `git commit -m "Description of changes"`.
4. Push your branch: `git push origin feature-name`.
5. Submit a pull request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Contact

For questions, suggestions, or collaboration opportunities, please contact **[Your Name]** at **[Your Email Address]**.

---
# Decoding Speculative Decoding

**Research Paper:** [https://arxiv.org/pdf/2402.01528v4](https://arxiv.org/pdf/2402.01528v4)

## The Mission
Large Language Models (LLMs) are computationally expensive and resource-intensive, limiting their accessibility and scalability for real-world applications such as education, healthcare, and customer support. This hinders the democratization of AI and its potential to benefit society broadly.

## Architecture
The solution involves building a scalable, production-ready inference system that leverages speculative decoding to speed up LLM inference. The architecture will use a two-model system: a lightweight, hardware-efficient draft model for speculative token generation and a larger target LLM for verification. The tech stack includes Python, PyTorch for model integration, TensorRT for hardware optimization, FastAPI for serving the models, Redis for caching, Docker for containerization, and Kubernetes for orchestration.

## Progress Log
- [x] Initial repository setup
- [ ] Implement draft model integration
- [ ] Implement target model verification
- [ ] Add speculative decoding logic
- [ ] Optimize with TensorRT
- [ ] Set up FastAPI for serving
- [ ] Integrate Redis caching
- [ ] Create Docker containerization
- [ ] Configure Kubernetes for orchestration

- **Completed Task:** Set up the project repository with basic folder structure, README, and initial configurations.
- **Completed Task:** Create Dockerfiles for both the draft model and target LLM, ensuring compatibility with TensorRT and GPU acceleration.
- **Completed Task:** Implement the draft model selection logic based on the research insights to optimize for latency and hardware efficiency.
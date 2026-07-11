# Deployment Guide for Speculative Decoding API

This guide covers deploying the Speculative Decoding API on popular cloud platforms (AWS, GCP, Azure) with cost optimization strategies.

## Prerequisites

1. **Docker**: Ensure Docker is installed and configured on your local machine.
2. **Kubernetes Cluster**: Set up a Kubernetes cluster on your preferred cloud platform (AWS EKS, GCP GKE, or Azure AKS).
3. **kubectl**: Install and configure `kubectl` to manage your Kubernetes cluster.
4. **Helm**: Install Helm for managing Kubernetes charts.
5. **Cloud CLI**: Install the CLI for your chosen cloud provider (e.g., AWS CLI, gcloud, or Azure CLI).

---

## Deployment Steps

### 1. Build Docker Images

Before deploying, build the Docker images for the API and push them to a container registry (e.g., Amazon ECR, Google Container Registry, or Azure Container Registry).

```bash
# Build the API Docker image
cd /path/to/project

docker build -t speculative-decoding-api:latest -f Dockerfile .

# Tag and push the image to your container registry
# Example for AWS ECR
docker tag speculative-decoding-api:latest <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/speculative-decoding-api:latest
aws ecr get-login-password --region <REGION> | docker login --username AWS --password-stdin <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com
docker push <AWS_ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/speculative-decoding-api:latest
```

### 2. Configure Kubernetes Cluster

#### AWS EKS

1. Create an EKS cluster using the AWS Management Console or AWS CLI.
2. Configure `kubectl` to connect to your EKS cluster:

```bash
aws eks update-kubeconfig --region <REGION> --name <CLUSTER_NAME>
```

#### GCP GKE

1. Create a GKE cluster using the GCP Console or `gcloud` CLI:

```bash
gcloud container clusters create <CLUSTER_NAME> --zone <ZONE>
```

2. Configure `kubectl` to connect to your GKE cluster:

```bash
gcloud container clusters get-credentials <CLUSTER_NAME> --zone <ZONE>
```

#### Azure AKS

1. Create an AKS cluster using the Azure Portal or `az` CLI:

```bash
az aks create --resource-group <RESOURCE_GROUP> --name <CLUSTER_NAME> --node-count 3 --enable-addons monitoring --generate-ssh-keys
```

2. Configure `kubectl` to connect to your AKS cluster:

```bash
az aks get-credentials --resource-group <RESOURCE_GROUP> --name <CLUSTER_NAME>
```

### 3. Deploy Using Helm

1. Navigate to the Helm chart directory:

```bash
cd kubernetes/helm/speculative-decoding-api
```

2. Update the `values.yaml` file with your container registry details:

```yaml
image:
  repository: <CONTAINER_REGISTRY>/speculative-decoding-api
  tag: latest
```

3. Install the Helm chart:

```bash
helm install speculative-decoding-api .
```

4. Verify the deployment:

```bash
kubectl get pods
kubectl get services
```

### 4. Configure Prometheus (Optional)

If Prometheus monitoring is enabled in the `values.yaml` file, ensure that the `prometheus/prometheus.yml` configuration file is correctly mounted in the Prometheus pod.

Access the Prometheus dashboard:

```bash
kubectl port-forward svc/prometheus 9090:9090
```

Open your browser and navigate to `http://localhost:9090`.

### 5. Expose the API

1. Obtain the external IP address of the LoadBalancer service:

```bash
kubectl get service speculative-decoding-api
```

2. Use the external IP to access the API endpoints.

---

## Cost Optimization Strategies

1. **Right-Sizing Instances**: Choose instance types that match your workload requirements. For example, use GPU-optimized instances for TensorRT-based workloads.
2. **Auto-Scaling**: Configure Horizontal Pod Autoscaler (HPA) to scale pods based on CPU and memory usage.
3. **Spot Instances**: Use spot/preemptible instances for non-critical workloads to save costs.
4. **Resource Requests and Limits**: Set appropriate resource requests and limits in the `values.yaml` file to avoid over-provisioning.
5. **Monitoring and Alerts**: Use Prometheus and Grafana to monitor resource usage and set up alerts for unusual spikes.
6. **Optimize Docker Images**: Use minimal base images (e.g., `python:3.9-slim`) and multi-stage builds to reduce image size and startup time.
7. **Leverage Reserved Instances**: If using AWS, consider Reserved Instances for long-term workloads.
8. **Use Regional Clusters**: Deploy clusters in regions with lower costs.

---

## Cleanup

To delete the deployment and free up resources:

```bash
helm uninstall speculative-decoding-api
```

For cloud-specific cluster deletion:

- **AWS EKS**: `aws eks delete-cluster --name <CLUSTER_NAME>`
- **GCP GKE**: `gcloud container clusters delete <CLUSTER_NAME> --zone <ZONE>`
- **Azure AKS**: `az aks delete --resource-group <RESOURCE_GROUP> --name <CLUSTER_NAME>`

---

For further assistance, refer to the official documentation of your cloud provider or contact the project maintainers.

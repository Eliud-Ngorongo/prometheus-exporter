# Eliud Njenga - Infrastructure Coding Challenge (DockerHub stats exporter)
---
## Overview
This Prometheus Exporter is written in Python to return metric values for the count of Docker images pulls in a specified DockerHub organization. The exporter runs on port 2113 and provides metrics on the /metrics endpoint.

## Prerequisites
Ensure you have the following tools installed and configured on your machine:

    Docker: 25.0.0+
    kubectl: 1.29+
    kind: 0.21.0+ (using Kubernetes cluster v1.29)
    bash: 4.2+
    curl: 8.6.0+

## Installation
1. Clone the repository:
   ``` bash
   git clone <repository-url>
   cd <repository-name>
   ```
2. Build docker image

   ```bash
   docker build -f app-python/Dockerfile -t prometheus_exporter .
   ```
3. Create Kind cluster
   ```bash
   kind create cluster
   ```
4. Load the newly built Docker image into the Kind cluster::
   ``` bash
   kind load docker-image prometheus_exporter:latest
   ```
5. Apply the Kubernetes manifests:
   ``` bash
   kubectl apply -f k8s-resources/
   ```
6. Check the status of deployed resources
   ```bash
   kubectl get pods
   kubectl get svc
   ```
## Usage
Once deployed, the exporter starts collecting metrics about Docker image pulls for the specified organization every 5 minutes. You can access the available metrics by querying the /metrics endpoint. We can establishes a temporary connection between your local machine and the service defined in the k8s manifest by running the following command:
```bash
kubectl port-forward service/camunda-app 2113:2113
```
After running the above command, you can access the metrics endpoint by running this endpont on your preferred browser:
``` 
localhost:2113/metrics
``` 
 OR using your terminal with the command:
 ``` bash
 curl http://localhost:2113/metrics
```
 The expected results will look somethings similar to this:
 ![Diagram of the Prometheus Exporter](images/prometheus_exporter.png)



---
# Conclusion

With this straightforward Prometheus Exporter, you can efficiently monitor DockerHub image pulls for your organization with ease. The detailed guide simplifies the setup and deployment process within a local Kind Kubernetes cluster. Start tracking image usage today to optimize your container management strategies seamlessly.

# Contact
For any further questions or issues, please contact Eliud Njenga at eliudnjenga@gmail.com
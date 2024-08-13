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
To run this application, make use of the included makefiles with each file and its purpose described below.
## Makefile

The main entry point to invoke different commands from the test framework:

- **make build**: Builds the app and pushes the docker image to local _kind_ registry
- **make check**: Checks all required tools are installed
- **make create**: Creates local kind cluster
- **make deploy**: Deploys the app
- **make full-test**: Runs the full testing suite
- **make help**: This help
- **make lint**: Runs linters, check missing TODOs
- **make teardown**: Destroys local kind cluster and registry
- **make test**: Runs basic tests to check that the app works (in the kind cluster)
- **make test-local**: Runs basic tests to check that the app works (non-dockerized)
- **make run**: Runs the app locally (non-dockerized)
- ** _You do not need to edit of the file above_**

## Altertenative Approach

1. Clone the repository:
   ``` bash
   git clone https://github.com/Eliud-Ngorongo/prometheus-exporter
   cd prometheus exporter
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


After running the above command, you can access the metrics endpoint by running this endpont on your preferred browser:
```
    localhost:2113/metrics
``` 
 OR using your terminal with the command:
 ``` 
 curl http://localhost:2113/metrics
```
 The expected results will look somethings similar to this:
 ![Diagram of the Prometheus Exporter](app-python/images/prometheus_exporter.png)


---
# Conclusion

With this straightforward Prometheus Exporter, you can efficiently monitor DockerHub image pulls for your organization with ease. The detailed guide simplifies the setup and deployment process within a local Kind Kubernetes cluster. Start tracking image usage today to optimize your container management strategies seamlessly.

# Contact
For any further questions or issues, please contact Eliud Njenga at eliudnjenga@gmail.com

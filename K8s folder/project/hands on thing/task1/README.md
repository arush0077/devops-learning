# Task 1: Apache Deployment on Kubernetes

This folder contains the necessary files to deploy an Apache web server on Kubernetes (Minikube) and expose it via an Ingress controller.

## Files Included

- `apache-deployment.yaml`: Kubernetes deployment configuration for Apache
- `apache-service.yaml`: Service configuration to expose the Apache deployment
- `apache-ingress.yaml`: Ingress configuration for domain routing

## Deployment Steps

### 1. Start Minikube

```bash
# Check minikube status
minikube status

# Start minikube if not running
minikube start --nodes=3

# Enable ingress addon
minikube addons enable ingress
```

### 2. Deploy Apache Web Server

```bash
# Apply the deployment and service
kubectl apply -f apache-ns.yml
kubectl apply -f apache-deployment.yaml
kubectl apply -f apache-service.yaml
```

### 3. Configure Ingress

```bash
# Apply the ingress configuration
kubectl apply -f apache-ingress.yaml
```

### 4. Access the Application

```bash
# Use port-forwarding to access the application directly Keep Terminal Running 
kubectl port-forward -n apache-ns svc/apache-service 8080:80

# Now you can access the application at:
# http://localhost:8080
```

This approach uses port-forwarding to directly connect to the service without needing to modify your hosts file. The service will be accessible at http://localhost:8080 while the port-forwarding is active.

Alternatively, you can run the provided setup script which will handle the deployment and port-forwarding for you:

Once port-forwarding is active, access the application in your browser at:
http://localhost:8080

### 5. Clear all

```bash

kubectl delete ns apache-ns

```


## Learning Outcomes

- Setting up and using Minikube for local Kubernetes development
- Creating Kubernetes deployments and services
- Configuring Ingress resources for external access
- Understanding Kubernetes YAML configuration files
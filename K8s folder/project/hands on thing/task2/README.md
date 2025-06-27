# Task 2: Self-Signed SSL Certificates for Kubernetes

This task focuses on creating self-signed SSL certificates to make your Kubernetes application appear as a proper secure website. This guide assumes you have already completed Task 1 and have an Apache deployment running.

## Prerequisites
- Complete Task 1 from Readme Deployment Till Step -2 [ Deploy Apache Web Server]

## Implementation Steps

### 1. Generate Self-Signed SSL Certificates

Follow these steps to manually create self-signed SSL certificates using OpenSSL on git bash or any linux based terminal (on windows it might cause problems):

```bash
# Create a directory for certificates
mkdir ssl-certs
cd ssl-certs

# Generate a private key
openssl genrsa -out tls.key 2048

# Generate a Certificate Signing Request (CSR)
openssl req -new -key tls.key -out tls.csr -subj "//CN=localhost/O=Example Organization/C=US"


# Generate a self-signed certificate valid for 365 days
openssl x509 -req -days 365 -in tls.csr -signkey tls.key -out tls.crt

# Create a Kubernetes TLS secret
kubectl create secret tls apache-tls --cert=tls.crt --key=tls.key -n apache-ns
```

### 2. Apply the Ingress Configuration

```bash
# Apply the ingress configuration with SSL

kubectl apply -f ./../apache-ingress-ssl.yaml
```

### 3. Access the Secure Application

To access the application securely with HTTPS, you need to set up port-forwarding to the Ingress controller, not directly to the service:

```bash
# Start port-forwarding to the ingress controller
kubectl port-forward -n ingress-nginx svc/ingress-nginx-controller 8443:443
```

While the port-forwarding is active, you can access the secure application at:

```
https://localhost:8443
```

### 5. Clean Up

When you're done, you can clean up the resources:

```bash

kubectl delete ns apache-ns

#Delete the folder created
cd ..
rm -rf ssl-certs/
```

## Learning Outcomes

- Creating and managing SSL certificates
- Configuring Ingress resources with TLS
- Understanding how HTTPS works in Kubernetes

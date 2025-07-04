# Simplified Kubernetes Ingress Component

This project demonstrates how to use Pulumi Component Resources to bundle logically related Kubernetes resources together. The `K8sIngress` component bundles an NGINX ingress controller and an ingress resource as a single logical unit, optimized for faster deployment.

## How to Use

1. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Deploy with Pulumi:
   ```
   pulumi up --yes
   ```

3. Apply the sample ingress resource:
   ```
   kubectl apply -f sample-ingress.yaml
   ```


## Testing Your Deployment

After running `pulumi up`, you can test your ingress deployment:

1. Check the status of your resources:
   ```
   kubectl -n ingress-nginx get ingress,service,pods
   ```

2. Apply the sample ingress resource:
   ```
   kubectl apply -f sample-ingress.yaml
   ```

3. Create a test deployment and service:
   ```
   kubectl create deployment example --image=nginx --port=80 -n ingress-nginx
   kubectl expose deployment example --name=example-service --port=80 -n ingress-nginx
   ```

4. Access your application:
   - If using LoadBalancer, access via the external IP (shown in Pulumi outputs)
   - If using NodePort, access via `http://<node-ip>:<node-port>`
   - If using Minikube, use port-forwarding:
     ```
     kubectl -n ingress-nginx port-forward svc/ingress-nginx-controller 8080:80
     ```


## Cleanup

```
pulumi destroy --yes
deactivate
```


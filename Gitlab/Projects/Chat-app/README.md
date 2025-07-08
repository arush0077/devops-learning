# Chat App Pulumi Deployment

## Prerequisites

- Python
- Pulumi
- Minikube
- kubectl

## Quick Start
1. git add .; git commit -m "All Ok"; git push;
2. Access the application: Once the pipeline is done
   ```
   kubectl port-forward -n ingress-nginx service/ingress-nginx-controller 8080:80 --address=0.0.0.0
   ```
   
   Then open in browser:
   - Frontend: `http://localhost:8080`
   - Backend API: `http://localhost:8080/api`

3. Run the Destroy job manually from GitLab CI/CD if needed
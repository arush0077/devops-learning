# Chat App Pulumi Deployment

## Prerequisites

- Python
- Pulumi
- Minikube
- kubectl

## Quick Start

1. Create a virtual environment and install dependencies:
   ```
   cd pulumi
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Create a new dev stack with empty passphrase:
   ```
   #Initialize stack if not auto detected 
   pulumi stack init dev 
   # Press <Enter> for passphrase when prompted
   pulumi stack select dev
   ```

3. Deploy with Pulumi:
   ```
   pulumi preview
   # Press <Enter> for passphrase when prompted
   pulumi up --yes
   # Press <Enter> for passphrase when prompted
   ```

4. Access the application:
   ```
   kubectl port-forward -n ingress-nginx service/ingress-nginx-controller 8080:80 --address=0.0.0.0
   ```
   
   Then open in browser:
   - Frontend: `http://localhost:8080`
   - Backend API: `http://localhost:8080/api`

## Cleanup

```
pulumi destroy --yes
deactivate
# Press <Enter> for passphrase when prompted

# Optional to clean the directories of python
rm -r .\venv\
Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force

```

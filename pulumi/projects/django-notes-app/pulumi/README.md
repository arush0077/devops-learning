# Notes App Pulumi Deployment

This directory contains Pulumi configuration to deploy the Notes App on Kubernetes (Minikube).

## Prerequisites

- Pulumi CLI installed (version >= 3.0.0)
- Minikube installed and running
- kubectl configured to work with Minikube
- Python 3.6 or later installed

## Files Structure

- `__main__.py` - Main Pulumi program file
- `Pulumi.yaml` - Pulumi project file
- `requirements.txt` - Python dependencies file
- `modules/` - Directory containing modular components
  - `__init__.py` - Python package marker
  - `config.py` - Configuration handling
  - `namespace.py` - Namespace resource creation
  - `deployment.py` - Templated deployment resources creation
  - `service.py` - Templated service resources creation
  - `ingress.py` - Ingress resource creation


## How to Use

### Setup After Cloning

When you clone this repository, follow these steps to set up the Pulumi project:

```bash
# Create and activate a virtual environment
python -m venv venv

# On Windows
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Select or create a new stack
pulumi stack select dev 
```

### Preview the Deployment

```bash
pulumi preview
#Press <Enter> for passphrase
```

### Deploy the Application

```bash
pulumi up --yes
#Press <Enter> for passphrase

```



### Access the Application

After deploying with Pulumi, run the following command to access the application:

```bash
kubectl port-forward svc/ingress-nginx-controller 8080:80 -n ingress-nginx --address=0.0.0.0
```

Then access:
- Notes App: http://localhost:8080
- Nginx: http://localhost:8080/nginx

### Destroy the Infrastructure

```bash
pulumi down --yes 
#Press <Enter> for passphrase
```

```bash
deactivate
rm -r .\venv\
```

```bash
Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
exit
```
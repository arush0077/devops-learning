# Notes App Pulumi Deployment

This Hands on focus on creating a grafana monitoring with help of pulumi.


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
pulumi up --yes --skip-preview
#Press <Enter> for passphrase

```



### Access the Application

After deploying with Pulumi, run the following command in other terminal to access the application:

```bash
kubectl port-forward svc/loki-service -n monitoring 3100:3100 #[optional]
kubectl port-forward svc/grafana-service -n monitoring 3000:80

```

Then access:
- Monitor on : http://localhost:3000/monitor
- Loki on : http://localhost:3100/ready [to check the loki ready or not]
- Go to data sources in the monitoring grafana and try loki with url -> http://loki-service.monitoring.svc.cluster.local:3100
- Go to data sources in the monitoring grafana and try prometheus with url -> http://prometheus-service.monitoring.svc.cluster.local:9090
- Import Dashboard from dashboard.json in the current folder

### Destroy the Infrastructure

```bash
pulumi destroy --yes  --skip-preview
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

---
### Conclusion


Finally we created a:

- pulumi project with the 
- grafana
- loki
- promtail
- node-exporter
- prometheus

and have the dahboard json to load a custom dashboard.

---


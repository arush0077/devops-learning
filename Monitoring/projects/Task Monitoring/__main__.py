import pulumi
import pulumi_kubernetes as k8s

# Create Namespace
monitoring_ns = k8s.core.v1.Namespace("monitoring",
    metadata={"name": "monitoring"}
)

# Deploy Grafana [Task 1]
grafana_labels = {"app": "grafana"}

grafana_deployment = k8s.apps.v1.Deployment("grafana-deployment",
    metadata={"namespace": monitoring_ns.metadata["name"]},
    spec={
        "selector": {"matchLabels": grafana_labels},
        "replicas": 1,
        "template": {
            "metadata": {"labels": grafana_labels},
            "spec": {
                "containers": [{
                    "name": "grafana",
                    "image": "grafana/grafana:latest",
                    "ports": [{"containerPort": 3000}]
                }]
            }
        }
    }
)

grafana_service = k8s.core.v1.Service("grafana-service",
    metadata={"namespace": monitoring_ns.metadata["name"], "name": "grafana-service"},
    spec={
        "selector": grafana_labels,
        "ports": [{"port": 80, "targetPort": 3000}],
        "type": "NodePort",       
    }
)



# Deploy Node Exporter (as an example exporter)
node_exporter_labels = {"app": "node-exporter"}

node_exporter_daemonset = k8s.apps.v1.DaemonSet("node-exporter",
    metadata={"namespace": monitoring_ns.metadata["name"]},
    spec={
        "selector": {"matchLabels": node_exporter_labels},
        "template": {
            "metadata": {"labels": node_exporter_labels},
            "spec": {
                "containers": [{
                    "name": "node-exporter",
                    "image": "prom/node-exporter:latest",
                    "ports": [{"containerPort": 9100}]
                }]
            }
        }
    }
)


# [Task 2]
grafana_ingress = k8s.networking.v1.Ingress("grafana-ingress",
    metadata={
        "namespace": monitoring_ns.metadata["name"],
        "annotations": {
            "nginx.ingress.kubernetes.io/rewrite-target": "/"
        }
    },
    spec={
        "rules": [{
            "http": {
                "paths": [{
                    "path": "/monitor",
                    "pathType": "Prefix",
                    "backend": {
                        "service": {
                            "name": grafana_service.metadata["name"],
                            "port": {"number": 80}
                        }
                    }
                }]
            }
        }]
    }
)




# Loki things from here -. [Task 3]
loki_labels = {"app": "loki"}

loki_deployment = k8s.apps.v1.Deployment("loki-deployment",
    metadata={"namespace": monitoring_ns.metadata["name"]},
    spec={
        "selector": {"matchLabels": loki_labels},
        "replicas": 1,
        "template": {
            "metadata": {"labels": loki_labels},
            "spec": {
                "containers": [{
                    "name": "loki",
                    "image": "grafana/loki:2.9.3",  
                    "args": ["-config.file=/etc/loki/local-config.yaml"],
                    "ports": [{"containerPort": 3100}]
                }]
            }
        }
    }
)

loki_service = k8s.core.v1.Service("loki-service",
    metadata={"namespace": monitoring_ns.metadata["name"],"name": "loki-service"},
    spec={
        "selector": loki_labels,
        "ports": [{"port": 3100, "targetPort": 3100}],
        "type": "ClusterIP"
    }
)


promtail_labels = {"app": "promtail"}

promtail_daemonset = k8s.apps.v1.DaemonSet("promtail",
    metadata={"namespace": monitoring_ns.metadata["name"]},
    spec={
        "selector": {"matchLabels": promtail_labels},
        "template": {
            "metadata": {"labels": promtail_labels},
            "spec": {
                "containers": [{
                    "name": "promtail",
                    "image": "grafana/promtail:2.9.3",
                    "args": ["-config.file=/etc/promtail/promtail-config.yaml"],
                    "volumeMounts": [
                        {"name": "config", "mountPath": "/etc/promtail"},
                        {"name": "varlog", "mountPath": "/var/log"},
                        {"name": "docker", "mountPath": "/var/lib/docker/containers", "readOnly": True}
                    ]
                }],
                "volumes": [
                    {
                        "name": "config",
                        "configMap": {
                            "name": "promtail-config"
                        }
                    },
                    {"name": "varlog", "hostPath": {"path": "/var/log"}},
                    {"name": "docker", "hostPath": {"path": "/var/lib/docker/containers"}}
                ]
            }
        }
    }
)


promtail_config = """
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki-service.monitoring.svc.cluster.local:3100/loki/api/v1/push

scrape_configs:
  - job_name: varlogs
    static_configs:
      - targets:
          - localhost
        labels:
          job: varlogs
          host: '${HOSTNAME}'
          __path__: /var/log/*.log

  - job_name: containerlogs
    static_configs:
      - targets:
          - localhost
        labels:
          job: containerlogs
          host: '${HOSTNAME}'
          __path__: /var/log/containers/*.log

  # Collect syslog specifically (optional)
  - job_name: syslog
    static_configs:
      - targets:
          - localhost
        labels:
          job: syslog
          host: '${HOSTNAME}'
          __path__: /var/log/syslog

  # Collect messages (optional)
  - job_name: messages
    static_configs:
      - targets:
          - localhost
        labels:
          job: messages
          host: '${HOSTNAME}'
          __path__: /var/log/messages

"""

promtail_cm = k8s.core.v1.ConfigMap("promtail-config",
    metadata={"namespace": monitoring_ns.metadata["name"], "name": "promtail-config"},
    data={"promtail-config.yaml": promtail_config}
)


pulumi.export("grafana-service-name", grafana_service.metadata["name"])


#Task  4 -> Make an dahboard inside it did it and tried well


#Task 5 -> Node exporter Prometheus data collector and showing it in a dashboard 

prometheus_config = """
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter.monitoring.svc.cluster.local:9100']
"""

prometheus_cm = k8s.core.v1.ConfigMap("prometheus-config",
    metadata={"namespace": monitoring_ns.metadata["name"], "name": "prometheus-config"},
    data={"prometheus.yml": prometheus_config}
)

prometheus_labels = {"app": "prometheus"}

prometheus_deployment = k8s.apps.v1.Deployment("prometheus",
    metadata={"namespace": monitoring_ns.metadata["name"]},
    spec={
        "selector": {"matchLabels": prometheus_labels},
        "replicas": 1,
        "template": {
            "metadata": {"labels": prometheus_labels},
            "spec": {
                "containers": [{
                    "name": "prometheus",
                    "image": "prom/prometheus:latest",
                    "ports": [{"containerPort": 9090}],
                    "volumeMounts": [{
                        "name": "config-volume",
                        "mountPath": "/etc/prometheus/"
                    }]
                }],
                "volumes": [{
                    "name": "config-volume",
                    "configMap": {
                        "name": prometheus_cm.metadata["name"]
                    }
                }]
            }
        }
    }
)

prometheus_service = k8s.core.v1.Service("prometheus-service",
    metadata={"namespace": monitoring_ns.metadata["name"],"name": "prometheus-service"},
    spec={
        "selector": prometheus_labels,
        "ports": [{
            "port": 9090,
            "targetPort": 9090
        }],
        "type": "NodePort"
    }
)


'''
Finally we created a 

pulumi project with the 
grafana
loki
promtail
node-exporter
prometheus

and have the dahboard json to load a custom dashboard


'''
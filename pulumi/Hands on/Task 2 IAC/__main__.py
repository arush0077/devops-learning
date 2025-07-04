import pulumi
from k8s_ingress import K8sIngress

ingress = K8sIngress(
    "ing",
    namespace="ingress-nginx",
    ingress_class_name="nginx",  # Fixed missing comma
    rules=[
        {
            "host": "example.com",
            "http": {
                "paths": [
                    {
                        "path": "/",
                        "pathType": "Prefix",
                        "backend": {
                            "service": {
                                "name": "example-service",
                                "port": {
                                    "number": 80
                                }
                            }
                        }
                    }
                ]
            }
        }
    ],
    controller_values={
        "controller": {
            "service": {
                "type": "LoadBalancer",
                "externalTrafficPolicy": "Local"
            },
            "resources": {
                "requests": {
                    "cpu": "100m",
                    "memory": "128Mi"
                },
                "limits": {
                    "cpu": "200m",
                    "memory": "256Mi"
                }
            },
            "replicaCount": 1,
            "minAvailable": 1,
            "config": {
                "keep-alive-requests": "10000",
                "upstream-keepalive-timeout": "120",
                "proxy-body-size": "8m"
            }
        }
    },
    ingress_annotations={
        "nginx.ingress.kubernetes.io/rewrite-target": "/"
    },
    create_namespace=False
)

pulumi.export("ingress_controller_url", ingress.get_controller_url())
pulumi.export("namespace", ingress.namespace)
pulumi.export("ingress_class_name", ingress.ingress_class_name)

try:
    pulumi.export("ingress_name", ingress.ingress.metadata.apply(lambda meta: meta["name"]))
except Exception as e:
    pulumi.log.warn(f"Could not export ingress name: {str(e)}")
pulumi.export("test_command", pulumi.Output.concat(
    "kubectl -n ", ingress.namespace, " get ingress,service,pods"
))
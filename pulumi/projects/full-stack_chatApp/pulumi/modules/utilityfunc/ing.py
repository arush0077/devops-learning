from pulumi_kubernetes.networking.v1 import Ingress
from pulumi import ResourceOptions

def create_ingress(name, namespace, rules, annotations=None, depends_on=None, enable_minikube_addon=False):
    resources = []

    if annotations is None:
        annotations = {"kubernetes.io/ingress.class": "nginx"}

    ingress = Ingress(
        name,
        metadata={
            "name": name,
            "namespace": namespace,
            "annotations": annotations
        },
        spec={
            "rules": rules
        },
        opts=ResourceOptions(depends_on=depends_on)
    )

    resources.append(ingress)

    return {
        "ingress": ingress,
        "resources": resources
    }

def create_http_rule(paths):
    return {
        "http": {
            "paths": paths
        }
    }

def create_path(path, path_type, service_name, service_port):
    return {
        "path": path,
        "pathType": path_type,
        "backend": {
            "service": {
                "name": service_name,
                "port": {
                    "number": service_port
                }
            }
        }
    }

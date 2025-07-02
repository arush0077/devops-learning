# components/deployment.py

from pulumi_kubernetes.apps.v1 import Deployment

def create_deployment(name_of_ns,name_of_image):
    app_labels = { "app": name_of_ns }
    return Deployment(
        name_of_ns + "-dep",
        metadata={ "namespace": name_of_ns },
        spec={
            "selector": { "match_labels": app_labels },
            "replicas": 1,
            "template": {
                "metadata": { "labels": app_labels },
                "spec": {
                    "containers": [{
                        "name": name_of_image+"-cont",
                        "image": name_of_image,
                        "ports": [{ "container_port": 80 }]
                    }]
                }
            }
        }
    )



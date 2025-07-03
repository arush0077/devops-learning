from pulumi_kubernetes.apps.v1 import Deployment
from pulumi import ResourceOptions

def create_deployment(name, namespace, image, replicas, port, labels=None, env_from=None, env=None, 
                     volume_mounts=None, volumes=None, depends_on=None):
    if labels is None:
        labels = {"app": name}
    
    if env_from is None:
        env_from = []
    
    if env is None:
        env = []
    
    if volume_mounts is None:
        volume_mounts = []
    
    if volumes is None:
        volumes = []
    
    container_spec = {
        "name": name,
        "image": image,
        "ports": [{"containerPort": port}],
    }
    
    if env_from:
        container_spec["envFrom"] = env_from
    
    if env:
        container_spec["env"] = env
    
    if volume_mounts:
        container_spec["volumeMounts"] = volume_mounts
    
    deployment_spec = {
        "replicas": replicas,
        "selector": {"matchLabels": labels},
        "template": {
            "metadata": {"labels": labels},
            "spec": {"containers": [container_spec]}
        }
    }
    
    if volumes:
        deployment_spec["template"]["spec"]["volumes"] = volumes
    
    deployment = Deployment(
        name,
        metadata={
            "name": name,
            "namespace": namespace
        },
        spec=deployment_spec,
        opts=ResourceOptions(depends_on=depends_on)
    )
    
    return deployment
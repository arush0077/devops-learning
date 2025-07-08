from pulumi_kubernetes.core.v1 import Service
from pulumi import ResourceOptions

def create_service(name, namespace, selector, port, target_port=None, service_type="ClusterIP", depends_on=None):
    if target_port is None:
        target_port = port
    
    service = Service(
        name,
        metadata={
            "name": name,
            "namespace": namespace
        },
        spec={
            "selector": selector,
            "ports": [{
                "port": port,
                "targetPort": target_port
            }],
            "type": service_type
        },
        opts=ResourceOptions(depends_on=depends_on)
    )
    
    return service
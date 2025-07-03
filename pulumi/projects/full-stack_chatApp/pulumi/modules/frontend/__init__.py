from .dep import create_frontend_deployment
from .svc import create_frontend_service

def create_frontend(namespace, image, replicas, port, config_map_name, depends_on=None):
    deployment = create_frontend_deployment(
        namespace=namespace,
        image=image,
        replicas=replicas,
        port=port,
        config_map_name=config_map_name,
        depends_on=depends_on
    )
    
    service = create_frontend_service(
        namespace=namespace,
        port=port,
        depends_on=[deployment]
    )
    
    return {
        "service_name": service.metadata["name"],
        "service_port": service.spec["ports"][0]["port"],
        "deployment_name": deployment.metadata["name"]
    }
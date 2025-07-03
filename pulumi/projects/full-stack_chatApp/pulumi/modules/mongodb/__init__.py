from .dep import create_mongodb_deployment
from .svc import create_mongodb_service
from ..utilityfunc.pv import create_persistent_volume, create_persistent_volume_claim
from pulumi import ResourceOptions

def create_mongodb(namespace, image, storage_size, root_username, root_password):
    pv = create_persistent_volume(
        name="mongodb-pv",
        storage_size=storage_size,
        host_path="/data"
    )
    
    pvc = create_persistent_volume_claim(
        name="mongodb-pvc",
        namespace=namespace,
        storage_size=storage_size,
        depends_on=[pv]
    )
    
    deployment = create_mongodb_deployment(
        namespace=namespace,
        image=image,
        pvc_name=pvc.metadata["name"],
        root_username=root_username,
        root_password=root_password,
        depends_on=[pvc]
    )
    
    service = create_mongodb_service(
        namespace=namespace,
        depends_on=[deployment]
    )
    
    return {
        "service_name": service.metadata["name"],
        "service_port": service.spec["ports"][0]["port"],
        "deployment_name": deployment.metadata["name"]
    }
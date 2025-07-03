from pulumi import ResourceOptions, Output
import pulumi
from ..utilityfunc.dep import create_deployment

def create_mongodb_deployment(namespace, image, pvc_name, root_username, root_password, depends_on=None):
    name = "chat-app-mongodb"
    labels = {"app": name}
    
    # Handle root_username and root_password as Pulumi Output objects
    env = pulumi.Output.all(root_username, root_password).apply(
        lambda args: [
            {
                "name": "MONGO_INITDB_ROOT_USERNAME",
                "value": args[0]
            },
            {
                "name": "MONGO_INITDB_ROOT_PASSWORD",
                "value": args[1]
            }
        ]
    )
    
    volume_mounts = [{
        "name": "mongodb-data",
        "mountPath": "/data/db"
    }]
    
    volumes = [{
        "name": "mongodb-data",
        "persistentVolumeClaim": {
            "claimName": pvc_name
        }
    }]
    
    deployment = create_deployment(
        name=name,
        namespace=namespace,
        image=image,
        replicas=1,
        port=27017,
        labels=labels,
        env=env,
        volume_mounts=volume_mounts,
        volumes=volumes,
        depends_on=depends_on
    )
    
    return deployment
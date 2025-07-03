from ..utilityfunc.dep import create_deployment

def create_backend_deployment(namespace, image, replicas, port, config_map_name, secret_name, depends_on=None):
    name = "chat-app-backend"
    labels = {"app": name}
    
    env_from = [
        {
            "configMapRef": {
                "name": config_map_name
            }
        },
        {
            "secretRef": {
                "name": secret_name
            }
        }
    ]
    
    deployment = create_deployment(
        name=name,
        namespace=namespace,
        image=image,
        replicas=replicas,
        port=port,
        labels=labels,
        env_from=env_from,
        depends_on=depends_on
    )
    
    return deployment
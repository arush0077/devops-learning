from ..utilityfunc.ing import create_ingress, create_http_rule, create_path

def create_ingress_resources(namespace, frontend_service_name, frontend_service_port, 
                           backend_service_name, backend_service_port, depends_on=None):
    paths = [
        create_path(
            path="/",
            path_type="Prefix",
            service_name=frontend_service_name,
            service_port=frontend_service_port
        ),
        create_path(
            path="/api",
            path_type="Prefix",
            service_name=backend_service_name,
            service_port=backend_service_port
        )
    ]
    
    rules = [create_http_rule(paths)]
    
    ingress_resources = create_ingress(
        name="chat-app-ingress",
        namespace=namespace,
        rules=rules,
        depends_on=depends_on,
        enable_minikube_addon=True
    )
    
    return {
        "ingress_name": ingress_resources["ingress"].metadata["name"]
    }
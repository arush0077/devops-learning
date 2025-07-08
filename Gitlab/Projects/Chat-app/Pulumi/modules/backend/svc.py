from ..utilityfunc.svc import create_service

def create_backend_service(namespace, port, depends_on=None):
    name = "backend"
    selector = {"app": "chat-app-backend"}
    
    service = create_service(
        name=name,
        namespace=namespace,
        selector=selector,
        port=port,
        target_port=port,
        depends_on=depends_on
    )
    
    return service
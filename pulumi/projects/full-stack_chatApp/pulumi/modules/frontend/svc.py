from ..utilityfunc.svc import create_service

def create_frontend_service(namespace, port, depends_on=None):
    name = "frontend"
    selector = {"app": "chat-app-frontend"}
    
    service = create_service(
        name=name,
        namespace=namespace,
        selector=selector,
        port=port,
        target_port=port,
        depends_on=depends_on
    )
    
    return service
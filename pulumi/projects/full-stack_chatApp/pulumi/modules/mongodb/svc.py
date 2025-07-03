from ..utilityfunc.svc import create_service

def create_mongodb_service(namespace, depends_on=None):
    name = "mongo"
    selector = {"app": "chat-app-mongodb"}
    
    service = create_service(
        name=name,
        namespace=namespace,
        selector=selector,
        port=27017,
        target_port=27017,
        depends_on=depends_on
    )
    
    return service
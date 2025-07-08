import pulumi

def get_config():
    config = pulumi.Config()

    namespace = config.get("namespace") or "chat-app"

    mongodb = {
        "image": config.get("mongodb_image") or "mongo",
        "storage_size": config.get("mongodb_storage_size") or "5Gi",
        "root_username": config.get_secret("mongodb_root_username") or "root",
        "root_password": config.get_secret("mongodb_root_password") or "admin"
    }

    backend = {
        "image": config.get("backend_image") or "arush75/chat-app-backend:v1",
        "replicas": config.get_int("backend_replicas") or 1,
        "port": config.get_int("backend_port") or 5001,
        "node_env": config.get("backend_node_env") or "production"
    }

    frontend = {
        "image": config.get("frontend_image") or "arush75/chat-app-frontend:v1",
        "replicas": config.get_int("frontend_replicas") or 1,
        "port": config.get_int("frontend_port") or 80
    }

    ingress = {
        "enabled": config.get_bool("ingress_enabled")
        if config.get("ingress_enabled") is not None else True
    }

    jwt_secret = config.get_secret("jwt_secret") or "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"

    return {
        "namespace": namespace,
        "mongodb": mongodb,
        "backend": backend,
        "frontend": frontend,
        "ingress": ingress,
        "jwt_secret": jwt_secret
    }

config = get_config()

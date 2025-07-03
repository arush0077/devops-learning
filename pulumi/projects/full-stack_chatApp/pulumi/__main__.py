import pulumi
from modules import (
    create_namespace,
    create_config_map,
    create_secret,
    create_mongodb,
    create_backend,
    create_frontend,
    create_ingress_resources
)
from config import config


namespace = create_namespace(config["namespace"])

config_map = create_config_map(
    name="chat-app-config",
    namespace=namespace.metadata["name"],
    data={
        "NODE_ENV": config["backend"]["node_env"],
        "PORT": str(config["backend"]["port"])
    }
)

# Get MongoDB credentials from config
root_username = config["mongodb"]["root_username"]
root_password = config["mongodb"]["root_password"]
jwt_secret = config['jwt_secret']

# Create MongoDB URI using the credentials
mongodb_uri = pulumi.Output.all(root_username, root_password).apply(
    lambda args: f"mongodb://{args[0]}:{args[1]}@mongo:27017/chatApp?authSource=admin"
)
secret = create_secret(
    name="chat-app-secret",
    namespace=namespace.metadata["name"],
    string_data={
        "MONGODB_URI": mongodb_uri,
        "JWT_SECRET": jwt_secret
    }
)

mongodb = create_mongodb(
    namespace=namespace.metadata["name"],
    image=config["mongodb"]["image"],
    storage_size=config["mongodb"]["storage_size"],
    root_username=config["mongodb"]["root_username"],
    root_password=config["mongodb"]["root_password"]
)

backend = create_backend(
    namespace=namespace.metadata["name"],
    image=config["backend"]["image"],
    replicas=config["backend"]["replicas"],
    port=config["backend"]["port"],
    config_map_name=config_map.metadata["name"],
    secret_name=secret.metadata["name"]
)

frontend = create_frontend(
    namespace=namespace.metadata["name"],
    image=config["frontend"]["image"],
    replicas=config["frontend"]["replicas"],
    port=config["frontend"]["port"],
    config_map_name=config_map.metadata["name"]
)

if config["ingress"]["enabled"]:
    ingress = create_ingress_resources(
        namespace=namespace.metadata["name"],
        frontend_service_name=frontend["service_name"],
        frontend_service_port=frontend["service_port"],
        backend_service_name=backend["service_name"],
        backend_service_port=backend["service_port"]
    )

pulumi.export("namespace", namespace.metadata["name"])
pulumi.export("Username", config["mongodb"]["root_username"].apply(lambda x: f"{x}"))
pulumi.export("Password", config["mongodb"]["root_password"].apply(lambda x: f"{x}"))
pulumi.export("frontend_service", frontend["service_name"])
pulumi.export("backend_service", backend["service_name"])
pulumi.export("mongodb_service", mongodb["service_name"])
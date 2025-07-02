import pulumi
from components.nginx.ns import create_namespace
from components.nginx.dep import create_deployment
from components.nginx.svc import create_service

# Get config values
config = pulumi.Config()
name_of_ns = config.require("namespace")
name_of_image = config.require("image")
port = int(config.get("port") or 80)            
target_port = int(config.get("targetPort") or 80)  

# Create resources
ns = create_namespace(name_of_ns)
deployment = create_deployment(name_of_ns, name_of_image)
service = create_service(name_of_ns, port, target_port)


username =config.get("username")
password =config.get_secret("password")
# Exports
pulumi.export("namespace", ns.metadata["name"])
pulumi.export("username", username)
pulumi.export("password_plain", password.apply(lambda p: str(p)))

pulumi.export("deployment_name", deployment.metadata["name"])
pulumi.export("service_name", service.metadata["name"])
pulumi.export("service_info", pulumi.Output.all(
    service.metadata["name"],
    service.spec
).apply(
    lambda args: f"{args[0]} is running on port {args[1]['ports'][0].get('nodePort', args[1]['ports'][0]['port'])}"
))

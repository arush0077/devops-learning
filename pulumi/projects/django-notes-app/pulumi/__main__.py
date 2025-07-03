import pulumi
from modules.config import get_config
from modules.namespace import create_namespace
from modules.deployment import create_deployment
from modules.service import create_service
from modules.ingress import create_ingress

# Get configuration
config_values = get_config()

# Create namespace
ns = create_namespace(config_values['namespace'])

# Define apps
apps = [
    {
        'name': 'notes-app',
        'image': config_values['notes_app_image'],
        'replicas': config_values['notes_app_replicas'],
        'port': config_values['notes_app_port']
    },
    {
        'name': 'nginx',
        'image': config_values['nginx_image'],
        'replicas': config_values['nginx_replicas'],
        'port': config_values['nginx_port']
    }
]

# Create deployments and services
deployments = {}
services = {}

for app in apps:
    # Create deployment
    deployments[app['name']] = create_deployment(
        app_name=app['name'],
        namespace=ns,
        image=app['image'],
        replicas=app['replicas'],
        port=app['port'],
        dependencies=[ns]
    )
    
    # Create service
    services[app['name']] = create_service(
        app_name=app['name'],
        namespace=ns,
        target_port=app['port'],
        dependencies=[deployments[app['name']]]
    )

# Create Ingress
ingress = create_ingress(
    namespace=ns,
    notes_app_service=services['notes-app'],
    nginx_service=services['nginx'],
    dependencies=[services['notes-app'], services['nginx']]
)

# Export values
pulumi.export('namespace_name', ns.metadata['name'])
pulumi.export('notes_app_service_name', services['notes-app'].metadata['name'])
pulumi.export('nginx_service_name', services['nginx'].metadata['name'])
pulumi.export('ingress_name', ingress.metadata['name'])
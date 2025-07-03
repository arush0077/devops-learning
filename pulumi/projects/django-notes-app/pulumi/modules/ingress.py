import pulumi
import pulumi_kubernetes as k8s

def create_ingress(namespace, notes_app_service, nginx_service, dependencies=None):
    ingress = k8s.networking.v1.Ingress(
        'notes-app-route',
        metadata={
            'name': 'notes-app-route',
            'namespace': namespace.metadata['name'],
            'annotations': {
                'nginx.ingress.kubernetes.io/rewrite-target': '/',
            },
        },
        spec={
            'rules': [{
                'http': {
                    'paths': [
                        {
                            'path': '/',
                            'pathType': 'Prefix',
                            'backend': {
                                'service': {
                                    'name': notes_app_service.metadata['name'],
                                    'port': {
                                        'number': 8000,
                                    },
                                },
                            },
                        },
                        {
                            'path': '/nginx',
                            'pathType': 'Prefix',
                            'backend': {
                                'service': {
                                    'name': nginx_service.metadata['name'],
                                    'port': {
                                        'number': 80,
                                    },
                                },
                            },
                        },
                    ],
                },
            }],
        },
        opts=pulumi.ResourceOptions(depends_on=dependencies or [])
    )
    
    return ingress
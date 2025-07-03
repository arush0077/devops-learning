import pulumi
import pulumi_kubernetes as k8s

def create_deployment(app_name, namespace, image, replicas, port, dependencies=None):
    deployment = k8s.apps.v1.Deployment(
        f'{app_name}-dep',
        metadata={
            'name': f'{app_name}-dep',
            'namespace': namespace.metadata['name'],
        },
        spec={
            'replicas': replicas,
            'selector': {
                'matchLabels': {
                    'app': app_name,
                },
            },
            'template': {
                'metadata': {
                    'labels': {
                        'app': app_name,
                    },
                },
                'spec': {
                    'containers': [{
                        'name': f'{app_name}-pod',
                        'image': image,
                        'ports': [{
                            'containerPort': port,
                        }],
                    }],
                },
            },
        },
        opts=pulumi.ResourceOptions(depends_on=dependencies or [])
    )
    
    return deployment


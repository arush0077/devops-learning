import pulumi
import pulumi_kubernetes as k8s

def create_service(app_name, namespace, target_port, dependencies=None):
    service = k8s.core.v1.Service(
        f'{app_name}-svc',
        metadata={
            'name': f'{app_name}-svc',
            'namespace': namespace.metadata['name'],
        },
        spec={
            'selector': {
                'app': app_name,
            },
            'ports': [{
                'port': target_port,
                'targetPort': target_port,
                'protocol': 'TCP',
            }],
        },
        opts=pulumi.ResourceOptions(depends_on=dependencies or [])
    )
    
    return service


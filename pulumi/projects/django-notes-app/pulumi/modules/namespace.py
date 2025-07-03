import pulumi
import pulumi_kubernetes as k8s

def create_namespace(namespace_name):
    ns = k8s.core.v1.Namespace(
        'notes-app-ns',
        metadata={
            'name': namespace_name,
        }
    )
    
    return ns
from pulumi_kubernetes.core.v1 import Namespace

def create_namespace(name):
    namespace = Namespace(
        f"{name}-namespace",
        metadata={"name": name}
    )
    
    return namespace
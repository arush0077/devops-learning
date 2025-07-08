from pulumi_kubernetes.core.v1 import ConfigMap, Secret

def create_config_map(name, namespace, data):
    config_map = ConfigMap(
        name,
        metadata={
            "name": name,
            "namespace": namespace
        },
        data=data
    )
    
    return config_map

def create_secret(name, namespace, string_data, secret_type="Opaque"):
    secret = Secret(
        name,
        metadata={
            "name": name,
            "namespace": namespace
        },
        type=secret_type,
        string_data=string_data
    )
    
    return secret
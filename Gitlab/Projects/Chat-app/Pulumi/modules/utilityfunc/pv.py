from pulumi_kubernetes.core.v1 import PersistentVolume, PersistentVolumeClaim
from pulumi import ResourceOptions

def create_persistent_volume(name, storage_size, host_path, access_modes=None):
    if access_modes is None:
        access_modes = ["ReadWriteOnce"]
    
    pv = PersistentVolume(
        name,
        metadata={
            "name": name
        },
        spec={
            "capacity": {
                "storage": storage_size
            },
            "accessModes": access_modes,
            "hostPath": {
                "path": host_path
            }
        }
    )
    
    return pv

def create_persistent_volume_claim(name, namespace, storage_size, access_modes=None, depends_on=None):
    if access_modes is None:
        access_modes = ["ReadWriteOnce"]
    
    pvc = PersistentVolumeClaim(
        name,
        metadata={
            "name": name,
            "namespace": namespace
        },
        spec={
            "accessModes": access_modes,
            "resources": {
                "requests": {
                    "storage": storage_size
                }
            }
        },
        opts=ResourceOptions(depends_on=depends_on)
    )
    
    return pvc